"""Verified one-time transfer of the already tested UCAMP project files."""
import base64
import hashlib
import io
import json
import lzma
from pathlib import Path, PurePosixPath
import zipfile

EXPECTED = '160adeebf3e24fc4bbdff7e28db93b0a41755055e408a53aa60fcebeeb085980'
ROOT = Path('Retos_M5/Semana4_SCRUM').resolve()
parts = [Path(f'.github/ucamp-s4-publication.part{i}') for i in range(8)]
if not all(p.is_file() for p in parts):
    raise SystemExit('Expected exactly eight publication parts; refusing partial transfer.')
blob = base64.b64decode(''.join(p.read_text(encoding='ascii').strip() for p in parts), validate=True)
if hashlib.sha256(blob).hexdigest() != EXPECTED:
    raise SystemExit('Publication checksum mismatch; nothing was written.')
entries = json.loads(lzma.decompress(blob))
if not isinstance(entries, dict) or len(entries) != 17:
    raise SystemExit('Unexpected publication manifest.')

def safe_name(name):
    rel = PurePosixPath(name)
    if not name or rel.is_absolute() or '..' in rel.parts or '\\' in name:
        raise ValueError('Unsafe publication path: ' + name)
    return rel

def decode(payload):
    if set(payload) == {'text'}:
        return payload['text'].encode('utf-8')
    if set(payload) == {'base64'}:
        return base64.b64decode(payload['base64'], validate=True)
    raise ValueError('Unsupported entry payload')

pending = []
for name, payload in entries.items():
    destination = ROOT.joinpath(safe_name(name)).resolve()
    if not destination.is_relative_to(ROOT):
        raise ValueError('Path escaped the project directory')
    if destination.exists():
        raise FileExistsError('Refusing to overwrite an existing project file: ' + name)
    if set(payload) == {'zip'}:
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for member, value in payload['zip'].items():
                safe_name(member)
                if member.startswith('word/fonts/'):
                    raise ValueError('Font distribution is not allowed')
                info = zipfile.ZipInfo(member, (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, decode(value))
        content = output.getvalue()
    else:
        content = decode(payload)
    pending.append((destination, content))
for destination, content in pending:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
print(f'Unpacked {len(pending)} verified files into {ROOT}')
