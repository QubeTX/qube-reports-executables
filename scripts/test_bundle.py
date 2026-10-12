"""Checks that the verifier rejects damaged or unexpected bundle contents."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from build_bundle import safe_member, verify


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


if __name__ == '__main__':
    unittest.main()
