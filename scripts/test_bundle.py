"""Checks that the verifier rejects damaged or unexpected bundle contents."""
import hashlib
import json
from pathlib import Path
import posixpath
import re
import tempfile
import unittest

from build_bundle import safe_member, verify
from bundle_layout import command_guides, platform_path


class BundleVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        folder = self.root / 'example'
        folder.mkdir()
        self.payload = folder / 'manual.md'
        self.payload.write_bytes(b'Published manual\n')
        digest = hashlib.sha256(self.payload.read_bytes()).hexdigest()
        self.checksums = folder / 'sha256.sum'
        self.checksums.write_text(f'{digest}  manual.md\n')
        self.manifest = {'products': [{'folder': 'example', 'assets': [], 'documentation': [
            {'path': 'manual.md', 'bytes': self.payload.stat().st_size, 'sha256': digest}
        ]}]}
        self.save_manifest()

    def save_manifest(self):
        (self.root / 'bundle-manifest.json').write_text(json.dumps(self.manifest))

    def test_valid_snapshot(self):
        verify(self.root)

    def test_tampered_document(self):
        self.payload.write_bytes(b'Changed\n')
        with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
            verify(self.root)

    def test_rewritten_checksum_still_fails_manifest(self):
        self.payload.write_bytes(b'Changed\n')
        digest = hashlib.sha256(self.payload.read_bytes()).hexdigest()
        self.checksums.write_text(f'{digest}  manual.md\n')
        with self.assertRaisesRegex(ValueError, 'Documentation manifest mismatch'):
            verify(self.root)

    def test_unexpected_payload(self):
        (self.payload.parent / 'unexpected.exe').write_bytes(b'not a release asset')
        with self.assertRaisesRegex(ValueError, 'Unexpected or missing files'):
            verify(self.root)

    def test_traversal(self):
        for path in ['../outside', '/absolute', 'C:/absolute', 'folder\\escape', 'folder/../../escape']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                safe_member(path)

    def test_product_folder_cannot_escape(self):
        self.manifest['products'][0]['folder'] = '../outside'
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'Unsafe archive member'):
            verify(self.root)


class PlatformLayoutTests(unittest.TestCase):
    def test_every_install_option_has_one_pasteable_line(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'bundle-manifest.json').read_bytes())
        spec = json.loads((root / 'bundle-spec.json').read_bytes())
        self.assertEqual(manifest['guide_format'], 'single-line')
        self.assertEqual(spec['guide_format'], manifest['guide_format'])
        for path, guide in command_guides(manifest).items():
            with self.subTest(path=path):
                blocks = re.findall(r'^```(?:powershell|sh)\n(.*?)\n```$', guide, re.M | re.S)
                self.assertTrue(blocks)
                for command in blocks:
                    self.assertEqual(len(command.splitlines()), 1)
                    self.assertTrue(command.strip())
                    self.assertNotIn('://', command)

    def test_sd300_windows_guides_reference_the_bundled_runtime(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'bundle-manifest.json').read_bytes())
        runtime, = manifest['prerequisites']
        self.assertEqual(hashlib.sha256((root / runtime['path']).read_bytes()).hexdigest(), runtime['sha256'])
        matched = []
        for name, guide in command_guides(manifest).items():
            if 'vc_redist.x64.exe' not in guide or '/Runtime/' in name:
                continue
            reference = re.search(r'Start-Process -FilePath "([^"]+vc_redist\.x64\.exe)"', guide)
            self.assertIsNotNone(reference, name)
            path = posixpath.join(posixpath.dirname(name), reference.group(1).replace('\\', '/'))
            self.assertEqual(posixpath.normpath(path), runtime['path'])
            matched.append(name)
        expected = [f'SD-300/Windows/x64/{edition}/{fmt}/README.md'
                    for edition in ('Corporate', 'Standard') for fmt in ('EXE', 'MSI')]
        expected.append('SD-300/Windows/x64/Portable/Desktop/ZIP/README.md')
        self.assertCountEqual(matched, expected)

    def test_product_first_windows_editions_have_local_install_commands(self):
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / 'bundle-spec.json').read_bytes())
        for product in spec['products']:
            entries = [{'path': f"{product['id']}/{platform_path(name)}"} for name in product['assets']]
            guides = command_guides({'products': [dict(product, assets=entries)]})
            for edition in ('Standard', 'Corporate'):
                for extension, command in [('MSI', 'msiexec.exe /i'), ('EXE', 'Start-Process')]:
                    folder = f"{product['id']}/Windows/x64/{edition}/{extension}"
                    names = [Path(e['path']).name for e in entries if e['path'].startswith(folder + '/')]
                    with self.subTest(folder=folder):
                        self.assertEqual(len(names), 1)
                        self.assertIn(command, guides[folder + '/README.md'])
                        self.assertIn(names[0], guides[folder + '/README.md'])

    def test_linux_desktop_architecture_and_libc(self):
        for target, expected in [('gnu-arm64', 'ARM64/glibc'), ('gnu-x86_64', 'x64/glibc'),
                                 ('musl-x86_64', 'x64/musl')]:
            name = f'sd300-gui-linux-{target}.tar.xz'
            self.assertEqual(str(platform_path(name)), f'Linux/{expected}/Portable/Desktop/TAR.XZ/{name}')
        with self.assertRaisesRegex(ValueError, 'No offline layout'):
            platform_path('sd300-gui-linux-musl-arm64.tar.xz')


if __name__ == '__main__':
    unittest.main()
