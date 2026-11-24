import hashlib
import os
from pathlib import Path
import shutil
import urllib.request
import zipfile

root = Path(os.environ['RUNNER_TEMP'])
archive = root / 'offline.zip'
url = 'https://github.com/QubeTX/qube-reports-executables/releases/download/v4.0.1/qubetx-offline-bundle.zip'
with urllib.request.urlopen(url, timeout=90) as response, archive.open('wb') as output:
    shutil.copyfileobj(response, output)
with archive.open('rb') as source:
    assert hashlib.file_digest(source, 'sha256').hexdigest() == '47adef3235eea2e9fcfbd7aa77523471706234b2f7434d9aff51785debec04cf'
with zipfile.ZipFile(archive) as bundle:
    bundle.extractall(root)
print('Verified and staged offline toolkit 4.0.1.')
