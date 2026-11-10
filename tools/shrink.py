# Comprimeert voorbeeldpagina-afbeeldingen in place. Ads q80, kleine ads q78, nieuwsbrieven max 900 px breed q78.
import sys, os, io, glob
from PIL import Image
root = sys.argv[1]; before = after = n = 0
for f in glob.glob(os.path.join(root, '*', 'img', '*.jpg')):
    name = os.path.basename(f)
    if name.startswith('og'): continue
    kind = 'mail' if name.startswith('mail') else ('small' if name.endswith('-s.jpg') else 'ad')
    limit = {'ad': 260_000, 'small': 90_000, 'mail': 420_000}[kind]
    sz = os.path.getsize(f)
    if sz <= limit: continue
    im = Image.open(f).convert('RGB')
    if kind == 'mail' and im.width > 900: im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    if kind == 'ad' and im.width > 1080: im = im.resize((1080, round(im.height * 1080 / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=80 if kind == 'ad' else 78, optimize=True, progressive=True)
    if b.tell() < sz:
        open(f, 'wb').write(b.getvalue()); before += sz; after += b.tell(); n += 1
print(f'{n} afbeeldingen: {before/1e6:.0f} MB -> {after/1e6:.0f} MB')
