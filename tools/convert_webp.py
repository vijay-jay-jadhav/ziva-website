# Ziva Studios — convert every image to web-ready WebP (2 sizes) + manifest
# Needs:  %pip install pillow-heif
SRC = r"D:\Chrome Downloads\Brochure All in All-20261113T092657Z-1-001\Portfolio_Brochure All in All"
OUT = r"D:\Chrome Downloads\ziva_web\images"

SIZES   = {'lg': 2400, 'sm': 800}   # longest side in px: lg = lightbox/full view, sm = gallery thumbnails
QUALITY = {'lg': 82,   'sm': 78}

import re, json, csv
from pathlib import Path
from PIL import Image, ImageOps
import pillow_heif; pillow_heif.register_heif_opener()
Image.MAX_IMAGE_PIXELS = None

SRC, OUT = Path(SRC), Path(OUT)
IMG_EXT = {'.jpg','.jpeg','.png','.webp','.heic','.heif','.tif','.tiff','.bmp'}
slug = lambda s: re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-') or 'img'

manifest, used, before, after, errors = [], set(), 0, 0, []
files = sorted(f for f in SRC.rglob('*') if f.is_file() and f.suffix.lower() in IMG_EXT)
print(f"{len(files)} images to convert...\n")

for n, f in enumerate(files, 1):
    rel_dir = f.parent.relative_to(SRC)
    folder = '/'.join(slug(p) for p in rel_dir.parts) or 'unsorted'
    base = slug(f.stem); name = base; k = 2
    while f"{folder}/{name}" in used:
        name = f"{base}-{k}"; k += 1
    used.add(f"{folder}/{name}")
    try:
        with Image.open(f) as im:
            im = ImageOps.exif_transpose(im)
            alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
            im = im.convert('RGBA' if alpha else 'RGB')
            w0, h0 = im.size
            row = dict(folder=folder, name=name, original=str(f.relative_to(SRC)), orig_w=w0, orig_h=h0,
                       orientation='landscape' if w0 > h0 * 1.05 else 'portrait' if h0 > w0 * 1.05 else 'square')
            for key, px in SIZES.items():
                out = OUT / key / folder / f"{name}.webp"
                out.parent.mkdir(parents=True, exist_ok=True)
                img = im.copy(); img.thumbnail((px, px), Image.LANCZOS)   # never upscales
                img.save(out, 'WEBP', quality=QUALITY[key], method=6)
                row[f'{key}_w'], row[f'{key}_h'] = img.size
                row[f'{key}_path'] = f"images/{key}/{folder}/{name}.webp"
                after += out.stat().st_size
            before += f.stat().st_size
            manifest.append(row)
    except Exception as e:
        errors.append((str(f.relative_to(SRC)), str(e)[:100]))
    if n % 25 == 0 or n == len(files):
        print(f"  {n}/{len(files)} done")

(OUT.parent / 'manifest.json').write_text(json.dumps(manifest, indent=1), encoding='utf-8')
with open(OUT.parent / 'manifest.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=manifest[0].keys()); w.writeheader(); w.writerows(manifest)

print(f"\nConverted {len(manifest)} images: {before/1e6:,.0f} MB  ->  {after/1e6:,.0f} MB (both sizes)")
print(f"Output: {OUT}")
for folder in sorted({r['folder'] for r in manifest}):
    print(f"  {folder:45s} {sum(r['folder']==folder for r in manifest)} images")
if errors:
    print("\nFAILED:"); [print("  ", e) for e in errors]
