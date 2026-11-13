# Ziva Studios website

Static site, hosted on GitHub Pages.

- `index.html` – home page (styles in `assets/site.css`)
- `paintings.html`, `sculptures.html`, `murals.html`, `miniature-statues.html`, `miniature-models.html`, `photography.html` – category pages (generated)
- `images/lg` (2400 px) and `images/sm` (800 px) – WebP photos
- `data/manifest.json` – every image with sizes; `data/gallery.json` – which images appear on which page, with titles

## Changing photos or titles
1. Edit the lists in `tools/build_gallery.py`
2. `python tools/build_gallery.py` then `python tools/build_pages.py`
