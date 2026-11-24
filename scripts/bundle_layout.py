"""Platform-first paths and local install commands for verified release assets."""
from collections import defaultdict
from pathlib import PurePosixPath
import posixpath


def platform_path(name):
    """Classify the explicitly supported upstream formats. Fail on a new target."""
    package = PurePosixPath(name)
    if len(package.parts) != 1 or not name.isascii() or not all(c.isalnum() or c in '-_.' for c in name):
        raise ValueError(f'Invalid release filename: {name}')
    command_type = 'Desktop' if '-gui-' in name else 'CLI'
    if '-x86_64-pc-windows-msvc' in name or '-windows-x64-' in name or '-windows-x86_64.' in name:
        if package.suffix in ('.msi', '.exe'):
            edition = 'Corporate' if '-corporate' in name else 'Standard'
            return PurePosixPath('Windows/x64', edition, package.suffix[1:].upper(), name)
        if name.endswith('.zip'):
            return PurePosixPath('Windows/x64/Portable', command_type, 'ZIP', name)
    if '-universal-apple-darwin' in name or '-macos-universal' in name:
        if package.suffix in ('.pkg', '.dmg'):
            return PurePosixPath('macOS/Universal/Standard', package.suffix[1:].upper(), name)
        if name.endswith('.zip') and command_type == 'Desktop':
            return PurePosixPath('macOS/Universal/Portable/Desktop/ZIP', name)
    for target, arch in [('aarch64-apple-darwin', 'Apple-Silicon'), ('x86_64-apple-darwin', 'Intel-x64')]:
        if name.endswith(f'-{target}.tar.xz'):
            return PurePosixPath('macOS', arch, 'Portable/CLI/TAR.XZ', name)
    linux_targets = {
        'x86_64-unknown-linux-gnu': ('x64', 'glibc'), 'linux-gnu-x86_64': ('x64', 'glibc'),
        'x86_64-unknown-linux-musl': ('x64', 'musl'), 'linux-musl-x86_64': ('x64', 'musl'),
        'aarch64-unknown-linux-gnu': ('ARM64', 'glibc'), 'linux-gnu-arm64': ('ARM64', 'glibc'),
    }
    for target, (arch, libc) in linux_targets.items():
        if name.endswith(f'-{target}.tar.xz'):
            return PurePosixPath('Linux', arch, libc, 'Portable', command_type, 'TAR.XZ', name)
    raise ValueError(f'No offline layout for {name}')


def windows_command(product, path, runtime, single_line):
    name = path.name
    steps = []
    desktop = 'Desktop' in path.parts
    if runtime and path.parts[:3] == runtime.parts[:3] and (desktop or path.suffix in ('.msi', '.exe')):
        installer = posixpath.relpath(runtime, path.parent).replace('/', '\\')
        setup = f'Start-Process -FilePath "{installer}" -Wait -ErrorAction Stop'
        missing = '-not (Test-Path -LiteralPath $runtime)'
        message = 'throw "The Microsoft x64 runtime is required for SD-300 Desktop."'
        if single_line:
            check = f'if ($setup.ExitCode -notin (0, 3010) -or {missing}) {{ {message} }}'
            guard = f'if ({missing}) {{ $setup = {setup} -PassThru; {check} }}'
        else:
            guard = f'if ({missing}) {{\n    {setup}\n    if ({missing}) {{ {message} }}\n}}'
        steps.extend([
            '$system = if ([Environment]::Is64BitProcess) { "System32" } else { "Sysnative" }',
            '$runtime = Join-Path $env:WINDIR "$system\\vcruntime140.dll"',
            guard,
        ])

    if path.suffix == '.msi':
        steps.append(f'msiexec.exe /i ".\\{name}"')
    elif path.suffix == '.exe':
        steps.append(f'Start-Process -FilePath ".\\{name}" -Wait')
    else:
        command = product['commands'][0]
        version = product['tag'].removeprefix('v')
        variant = 'desktop' if desktop else 'cli'
        exe = 'sd300-gui' if desktop else command
        steps.extend([
            f'$dest = Join-Path $env:LOCALAPPDATA "QubeTX\\Portable\\{command}\\{version}\\{variant}"',
            f'Expand-Archive -LiteralPath ".\\{name}" -DestinationPath $dest -ErrorAction Stop',
            f'& "$dest\\{exe}.exe"' + ('' if desktop else ' --version'),
        ])
    if single_line and len(steps) > 1:
        return '& { ' + '; '.join(steps) + ' }'
    return '\n'.join(steps)


def unix_command(product, path, single_line):
    name = path.name
    command = product['commands'][0]
    if path.suffix == '.pkg':
        return f'sudo /usr/sbin/installer -pkg "./{name}" -target /'
    if path.suffix == '.dmg':
        attach = f'hdiutil attach -readonly -nobrowse -mountpoint "$mount_dir" "./{name}"'
        install = f'sudo /usr/sbin/installer -pkg "$mount_dir/{command}.pkg" -target /'
        cleanup = 'hdiutil detach "$mount_dir" && rmdir "$mount_dir"'
        if single_line:
            # Scope the traps to this paste. Keep the installer's exit status during cleanup.
            chain = ['mount_dir=$(mktemp -d)', """trap 'rmdir "$mount_dir" || exit 1' 0""", attach,
                     f"trap '{cleanup} || exit 1' 0", install]
            return '(' + ' && '.join(chain) + ')'
        return f'mount_dir=$(mktemp -d)\n{attach} &&\n  {install}\n{cleanup}'

    desktop = 'Desktop' in path.parts
    version = product['tag'].removeprefix('v')
    variant = 'desktop' if desktop else 'cli'
    dest = f'dest="$HOME/.local/opt/qubetx/{command}/{version}/{variant}"'
    if desktop and 'macOS' in path.parts:
        extract = f'ditto -x -k "./{name}" "$dest"'
        launch = 'open "$dest/SD-300.app"'
    else:
        executable = 'sd300/bin/sd300-gui' if desktop else f'{name.removesuffix(".tar.xz")}/{command}'
        extract = f'tar -xf "./{name}" -C "$dest"'
        launch = f'"$dest/{executable}"' + ('' if desktop else ' --version')
    steps = ['mkdir -p "$dest"', extract, launch]
    if single_line:
        return '(' + ' && '.join([dest, *steps]) + ')'
    return dest + '\n' + ' &&\n  '.join(steps)


def command_guides(manifest):
    """Write the guide format declared by the snapshot; older snapshots used multiple lines."""
    guide_format = manifest.get('guide_format', 'multiline')
    if guide_format not in ('multiline', 'single-line'):
        raise ValueError(f'Unknown guide format: {guide_format}')
    single_line = guide_format == 'single-line'
    sections = defaultdict(list)
    runtime = next((PurePosixPath(item['path']) for item in manifest.get('prerequisites', [])
                    if item['path'] == 'SD-300/Windows/x64/Runtime/vc_redist.x64.exe'), None)
    if runtime:
        sections[runtime.parent].append(
            '## Microsoft Visual C++ x64 runtime\n\n```powershell\n'
            'Start-Process -FilePath ".\\vc_redist.x64.exe" -Wait\n```\n')
    for product in manifest['products']:
        for asset in product['assets']:
            path = PurePosixPath(asset['path'])
            if 'Windows' in path.parts:
                shell = 'powershell'
                command = windows_command(product, path, runtime, single_line)
            else:
                shell = 'sh'
                command = unix_command(product, path, single_line)
            sections[path.parent].append(f"## {product['id']} {product['tag']}\n\n```{shell}\n{command}\n```\n")
    return {(folder / 'README.md').as_posix(): '\n'.join(blocks) for folder, blocks in sorted(sections.items())}
