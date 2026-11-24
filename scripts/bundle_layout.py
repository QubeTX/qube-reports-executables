"""Platform-first paths and local install commands for verified release assets."""
from collections import defaultdict
from pathlib import PurePosixPath


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


def install_commands(product, path):
    name = path.name
    command = product['commands'][0]
    version = product['tag'].removeprefix('v')
    if path.suffix == '.msi':
        return [f'msiexec.exe /i ".\\{name}"']
    if path.suffix == '.exe':
        return [f'Start-Process -FilePath ".\\{name}" -Wait']
    if path.suffix == '.pkg':
        return [f'sudo /usr/sbin/installer -pkg "./{name}" -target /']
    if path.suffix == '.dmg':
        return ['mount_dir=$(mktemp -d)',
                f'hdiutil attach -readonly -nobrowse -mountpoint "$mount_dir" "./{name}" &&',
                f'  sudo /usr/sbin/installer -pkg "$mount_dir/{command}.pkg" -target /',
                'hdiutil detach "$mount_dir" && rmdir "$mount_dir"']

    desktop = 'Desktop' in path.parts
    variant = 'desktop' if desktop else 'cli'
    if 'Windows' in path.parts:
        exe = 'sd300-gui' if desktop else command
        launch = f'& "$dest\\{exe}.exe"' + ('' if desktop else ' --version')
        return [f'$dest = Join-Path $env:LOCALAPPDATA "QubeTX\\Portable\\{command}\\{version}\\{variant}"',
                f'Expand-Archive -LiteralPath ".\\{name}" -DestinationPath $dest -ErrorAction Stop', launch]
    destination = f'$HOME/.local/opt/qubetx/{command}/{version}/{variant}'
    if desktop and 'macOS' in path.parts:
        return [f'dest="{destination}"', 'mkdir -p "$dest" &&',
                f'  ditto -x -k "./{name}" "$dest" &&', '  open "$dest/SD-300.app"']
    executable = 'sd300/bin/sd300-gui' if desktop else f'{name.removesuffix(".tar.xz")}/{command}'
    return [f'dest="{destination}"', 'mkdir -p "$dest" &&',
            f'  tar -xf "./{name}" -C "$dest" &&',
            f'  "$dest/{executable}"' + ('' if desktop else ' --version')]


def command_guides(manifest):
    """Write local commands for each product, target and installer format."""
    sections = defaultdict(list)
    for product in manifest['products']:
        for asset in product['assets']:
            path = PurePosixPath(asset['path'])
            shell = 'powershell' if 'Windows' in path.parts else 'sh'
            commands = '\n'.join(install_commands(product, path))
            fence = "```"
            sections[path.parent].append(f"## {product['id']} {product['tag']}\n\n{fence}{shell}\n{commands}\n{fence}\n")
    return {(folder / 'README.md').as_posix(): '\n'.join(blocks) for folder, blocks in sorted(sections.items())}
