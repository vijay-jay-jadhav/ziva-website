# Ziva Studios — contact sheets (thumbnail grids) per folder
# Run once first:  !pip install pillow-heif
ROOT = r"D:\Chrome Downloads\Brochure All in All-20261113T092657Z-1-001"
OUT  = r"D:\Chrome Downloads\ziva_contact_sheets"

from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import pillow_heif; pillow_heif.register_heif_opener()
Image.MAX_IMAGE_PIXELS = None

ROOT, OUT = Path(ROOT), Path(OUT); OUT.mkdir(exist_ok=True)
IMG_EXT = {'.jpg','.jpeg','.png','.webp','.heic','.heif','.tif','.tiff'}
CELL, PAD, LABEL, COLS, PER_SHEET = 300, 10, 34, 6, 36
try:
    font = ImageFont.truetype("arial.ttf", 13)
except OSError:
    font = ImageFont.load_default()

folders = {}
for f in sorted(ROOT.rglob('*')):
    if f.is_file() and f.suffix.lower() in IMG_EXT:
        folders.setdefault(f.parent, []).append(f)

heic_rows = []
for folder, files in folders.items():
    name = str(folder.relative_to(ROOT)).replace('\\', ' - ').replace('/', ' - ') or 'root'
    for part in range(0, len(files), PER_SHEET):
        chunk = files[part:part + PER_SHEET]
        rows = -(-len(chunk) // COLS)
        sheet = Image.new('RGB', (COLS * (CELL + PAD) + PAD, rows * (CELL + LABEL + PAD) + PAD + 40), 'white')
        d = ImageDraw.Draw(sheet)
        d.text((PAD, 12), f"{name}  ({part + 1}-{part + len(chunk)} of {len(files)})", fill='black', font=font)
        for i, f in enumerate(chunk):
            x = PAD + (i % COLS) * (CELL + PAD)
            y = 40 + PAD + (i // COLS) * (CELL + LABEL + PAD)
            try:
                with Image.open(f) as im:
                    im = ImageOps.exif_transpose(im)
                    if f.suffix.lower() in ('.heic', '.heif'):
                        heic_rows.append((name, f.name, im.width, im.height))
                    im.draft('RGB', (CELL * 2, CELL * 2))
                    im = im.convert('RGB'); im.thumbnail((CELL, CELL))
                    sheet.paste(im, (x + (CELL - im.width) // 2, y + (CELL - im.height) // 2))
            except Exception as e:
                d.rectangle([x, y, x + CELL, y + CELL], outline='red')
                d.text((x + 5, y + 5), "ERROR", fill='red', font=font)
            label = f.name if len(f.name) <= 40 else f.name[:37] + '...'
            d.text((x, y + CELL + 4), label, fill='black', font=font)
        out = OUT / f"{name}_{part // PER_SHEET + 1}.jpg"
        sheet.save(out, quality=72, optimize=True)
        print("saved", out.name, f"({out.stat().st_size // 1024} KB)")

print("\n=== HEIC resolutions ===")
for name, fn, w, h in heic_rows:
    print(f"{name} | {fn} | {w}x{h} | {'L' if w > h * 1.05 else 'P' if h > w * 1.05 else 'S'}")
