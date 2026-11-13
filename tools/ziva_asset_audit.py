# Ziva Studios — asset folder audit
# 1) Set ROOT to your folder path, then Run All.
ROOT = r"D:\Chrome Downloads\Brochure All in All-20261113T092657Z-1-001"

# pip install pillow pandas   (run once if missing)
import os, hashlib, pandas as pd
from pathlib import Path
from collections import Counter
from PIL import Image, ImageOps, ExifTags
Image.MAX_IMAGE_PIXELS = None
try:
    import pillow_heif; pillow_heif.register_heif_opener()   # optional, for .heic
except ImportError:
    pass
ROOT = Path(ROOT)
assert ROOT.exists(), f"Folder not found: {ROOT}"
IMG_EXT = {'.jpg','.jpeg','.png','.webp','.tif','.tiff','.bmp','.gif','.heic','.heif'}
VID_EXT = {'.mp4','.mov','.avi','.mkv','.webm','.m4v'}
def human(n):
    for u in ['B','KB','MB','GB']:
        if n < 1024: return f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}TB"
print("Root:", ROOT)

# 2) Folder tree (folders with file counts and size)
def tree(p, prefix=""):
    dirs = sorted([d for d in p.iterdir() if d.is_dir() and not d.name.startswith('.')], key=lambda x: x.name.lower())
    files = [f for f in p.iterdir() if f.is_file() and not f.name.startswith('.')]
    for i, d in enumerate(dirs):
        allf = [f for f in d.rglob('*') if f.is_file() and not f.name.startswith('.')]
        own = [f for f in d.iterdir() if f.is_file() and not f.name.startswith('.')]
        last = i == len(dirs) - 1
        print(f"{prefix}{'└── ' if last else '├── '}{d.name}/  [{len(own)} files here, {len(allf)} total, {human(sum(f.stat().st_size for f in allf))}]")
        tree(d, prefix + ('    ' if last else '│   '))
top = [f for f in ROOT.iterdir() if f.is_file() and not f.name.startswith('.')]
print(f"{ROOT.name}/  [{len(top)} loose files at top level]")
tree(ROOT)

# 3) Scan every file
ORIENT_TAG = next(k for k, v in ExifTags.TAGS.items() if v == 'Orientation')
rows = []
for f in sorted(ROOT.rglob('*')):
    if not f.is_file() or f.name.startswith('.'): continue
    rel = f.relative_to(ROOT)
    ext = f.suffix.lower()
    r = dict(section=rel.parts[0] if len(rel.parts) > 1 else '(root)',
             subfolder=str(rel.parent), file=f.name, ext=ext,
             kind='image' if ext in IMG_EXT else 'video' if ext in VID_EXT else 'pdf' if ext == '.pdf' else 'other',
             bytes=f.stat().st_size, size=human(f.stat().st_size))
    h = hashlib.md5()
    with open(f, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''): h.update(chunk)
    r['md5'] = h.hexdigest()
    if r['kind'] == 'image':
        try:
            with Image.open(f) as im:
                exif_o = (im.getexif() or {}).get(ORIENT_TAG, 1)
                w, hgt = ImageOps.exif_transpose(im).size if exif_o in (5,6,7,8) else im.size
                dpi = im.info.get('dpi', (None,))[0]
                r.update(width=w, height=hgt, megapixels=round(w*hgt/1e6, 1),
                         aspect=round(w/hgt, 2),
                         orientation='landscape' if w > hgt*1.05 else 'portrait' if hgt > w*1.05 else 'square',
                         mode=im.mode, dpi=round(dpi) if dpi else None, exif_rotated=exif_o != 1)
        except Exception as e:
            r['error'] = str(e)[:80]
    rows.append(r)
df = pd.DataFrame(rows)
df.to_csv(ROOT.parent / 'ziva_asset_inventory.csv', index=False)
print(f"Scanned {len(df)} files, {human(df.bytes.sum())}. CSV saved to: {ROOT.parent / 'ziva_asset_inventory.csv'}")

# 4) Summary by section (top-level folder)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); pd.set_option('display.max_rows', 500)
img = df[df.kind == 'image']
print("=== FILE TYPES OVERALL ===")
print(df.ext.value_counts().to_string(), "\n")
summ = df.groupby('section').agg(files=('file','count'), total_MB=('bytes', lambda b: round(b.sum()/1e6, 1)))
if len(img):
    s2 = img.groupby('section').agg(images=('file','count'), min_w=('width','min'), max_w=('width','max'),
            median_w=('width','median'), median_h=('height','median'), avg_MB=('bytes', lambda b: round(b.mean()/1e6, 2)),
            landscape=('orientation', lambda o: (o=='landscape').sum()), portrait=('orientation', lambda o: (o=='portrait').sum()),
            square=('orientation', lambda o: (o=='square').sum()))
    summ = summ.join(s2)
print("=== BY SECTION ===")
print(summ.to_string(), "\n")
print("=== BY SUBFOLDER ===")
print(df.groupby(['subfolder','kind']).size().unstack(fill_value=0).to_string())

# 5) Every file, one line each (paste this output to Claude)
cols = ['subfolder','file','size','width','height','orientation','aspect','mode','dpi']
cols = [c for c in cols if c in df.columns]
for sub, g in df.groupby('subfolder'):
    print(f"\n--- {sub}  ({len(g)} files) ---")
    print(g[cols[1:]].to_string(index=False))

# 6) Flags: problems to fix before web use
print("=== DUPLICATES (same content) ===")
dup = df[df.duplicated('md5', keep=False)].sort_values('md5')
print(dup[['subfolder','file','size']].to_string(index=False) if len(dup) else "None")
if len(img):
    print("\n=== HEAVY IMAGES (> 2 MB, need compression) ===", (img.bytes > 2e6).sum())
    print("=== SMALL IMAGES (< 1200 px long side, may look soft full-width) ===")
    small = img[img[['width','height']].max(axis=1) < 1200]
    print(small[['subfolder','file','width','height']].to_string(index=False) if len(small) else "None")
    print("\n=== NON-RGB modes (CMYK etc.) ===")
    odd = img[~img['mode'].isin(['RGB','RGBA','L','P'])]
    print(odd[['subfolder','file','mode']].to_string(index=False) if len(odd) else "None")
    print("\nEXIF-rotated images:", int(img.exif_rotated.sum()))
if 'error' in df: print("\n=== UNREADABLE ===\n", df[df.error.notna()][['subfolder','file','error']].to_string(index=False))
print("\n=== NON-IMAGE FILES ===")
oth = df[df.kind != 'image']
print(oth[['subfolder','file','kind','size']].to_string(index=False) if len(oth) else "None")
