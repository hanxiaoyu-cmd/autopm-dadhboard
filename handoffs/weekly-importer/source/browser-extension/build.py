"""Package the standalone extension using an explicit allowlist; never include settings."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'browser-extension/airtable-token-helper'
FILES = ['manifest.json', 'core.js', 'controller.js', 'service-worker.js', 'page.js',
         'index.html', 'help.html', 'styles.css', 'scopes.json', 'README.md', 'PRIVACY.md',
         *[f'icons/icon-{size}.png' for size in (16, 32, 48, 128)]]
sys.path.insert(0, str(ROOT))
from autopm.config import load_settings

settings = load_settings()
contents = {name: (SOURCE / name).read_bytes() for name in FILES}
for key in ('airtable_token', 'deepseek_api_key'):
    value = settings.get(key)
    if value and any(value.encode() in data for data in contents.values()):
        raise RuntimeError('Package contains a configured secret; aborted')
manifest = json.loads(contents['manifest.json'])
assert set(manifest['permissions']) == {'storage', 'identity', 'clipboardWrite'}
assert set(manifest['host_permissions']) == {'https://api.airtable.com/*', 'https://airtable.com/*'}
assert not any(key in manifest for key in ('content_scripts', 'externally_connectable', 'oauth2'))
assert manifest['background']['type'] == 'module'
for icon in manifest['icons'].values():
    assert contents[icon].startswith(b'\x89PNG\r\n\x1a\n')
archive = ROOT / 'dist/AutoPM_Airtable_Token_Helper.zip'
archive.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, data in contents.items():
        z.writestr(name, data)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == set(FILES)
    assert all(z.read(name) == data for name, data in contents.items())
report = {'archive': str(archive), 'version': manifest['version'], 'file_count': len(FILES),
          'bytes': archive.stat().st_size, 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
          'configured_secrets_absent': True, 'zip_integrity_passed': True,
          'source_bytes_match_archive': True, 'files': FILES}
out = ROOT / 'outputs/airtable-token-extension-20260909'
out.mkdir(parents=True, exist_ok=True)
(out / 'package-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=True, indent=2))
