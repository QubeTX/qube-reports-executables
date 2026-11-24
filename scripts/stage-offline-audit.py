import hashlib
import os
from pathlib import Path
import shutil
import urllib.request
import zipfile

root = Path(os.environ['RUNNER_TEMP'])
archive = root / 'offline.zip'
url = 'https://github.com/QubeTX/qube-reports-executables/releases/download/v4.0.0/qubetx-offline-bundle.zip'
with urllib.request.urlopen(url, timeout=90) as response, archive.open('wb') as output:
    shutil.copyfileobj(response, output)
with archive.open('rb') as source:
    assert hashlib.file_digest(source, 'sha256').hexdigest() == '97cd8dc4ec18c644d8422bdef9c298db4b8dda9f875294389d557be84dc8d88a'
with zipfile.ZipFile(archive) as bundle:
    bundle.extractall(root)
print('Verified and staged offline toolkit 4.0.0.')
