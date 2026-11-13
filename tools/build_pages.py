# Generates the six category pages from data/gallery.json.  Run:  python tools/build_pages.py
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
import hashlib
VER = hashlib.md5(b''.join((ROOT / f).read_bytes() for f in ('assets/site.css', 'assets/gallery.css', 'assets/gallery.js'))).hexdigest()[:8]
G = json.loads((ROOT / 'data/gallery.json').read_text(encoding='utf-8'))

PAGES = [  # slug, nav label, colour, eyebrow, h1, lede, note, layout
 ('paintings', 'Paintings', '--ultra', 'Arts Studio · Paintings', 'Paintings',
  'Portraits, historical and devotional works in Old Master oils on 100% linen canvas, framed behind museum-grade glass so they last for generations.',
  'Every frame here left the studio for someone’s wall.', 'salon'),
 ('sculptures', 'Sculptures', '--cad', 'Arts Studio · Sculptures', 'Sculptures',
  'Busts, standing figures and full stage sets. Modelled in clay first, then cast in fibre, bronze finish or Maharashtra’s own basalt.',
  'From a lump of clay to a life-size figure.', 'plinths'),
 ('murals', 'Murals', '--rose', 'Arts Studio · Murals', 'Murals & reliefs',
  'Festival gates, medallion walls and relief murals: large work for public spaces, scaled up square by square from a sketch.',
  'Keep scrolling. The wall moves sideways.', 'hscroll'),
 ('miniature-statues', 'Miniature Statues', '--sap', 'Arts Studio · Gifting', 'Miniature statues',
  'Small hand-finished figures made as keepsakes, awards and corporate gifts. Each one can be made in your colours, sizes and quantities.',
  'Pick one, and we will make it yours.', 'shelf'),
 ('miniature-models', 'Miniature Models', '--ultra', 'Arts Studio · Scale models', 'Miniature models',
  'Scale models of halls, temples and campuses for presentations and display, built by hand down to the painted panels on the walls.',
  'One temple hall, twelve angles.', 'viewer'),
 ('photography', 'Photography', '--rose', 'Filmmaking · Photography', 'Photography',
  'Thirty places across Raigad district, from sea forts to ghats, photographed for a large-format print series.',
  'Hover a pin, then click to open the photo.', 'atlas'),
]

def e(s): return html.escape(s, quote=True)

def nav(cur):
    items = ''.join(f'<a href="{s}.html"{" aria-current=\"page\"" if s == cur else ""}><span class="dot" style="background:var({c})"></span>{l}</a>'
                    for s, l, c, *_ in PAGES)
    return f'''<header class="nav">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Ziva studio space, home"><img class="lg-l" src="assets/logo/ziva-logo.png" alt="Ziva studio space"></a>
    <button class="theme-btn" id="themeBtn" aria-label="Switch light or dark mode" title="Light / dark"><svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg><svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg></button>
    <button class="btn ghost menu-btn" id="menuBtn" aria-expanded="false" aria-controls="links">Menu</button>
    <ul class="links" id="links">
      <li><a href="index.html">Home</a></li>
      <li class="dd"><button aria-haspopup="true">Work ▾</button><div class="dd-menu">{items}</div></li>
      <li class="dd"><button aria-haspopup="true">Divisions ▾</button><div class="dd-menu"><a href="design-lab.html"><span class="dot" style="background:var(--ultra)"></span>Design Lab</a><a href="filmmaking.html"><span class="dot" style="background:var(--rose)"></span>Filmmaking</a><a href="arts-studio.html"><span class="dot" style="background:var(--cad)"></span>Arts Studio</a></div></li>
      <li><a href="index.html#about">About</a></li>
      <li><a href="index.html#contact">Contact</a></li>
    </ul>
    <a class="btn cta" href="index.html#contact">Start a project</a>
  </div>
</header>'''

FOOT = '''<footer>
  <div class="wrap">
    <div class="foot-top">
      <nav aria-label="Footer"><a href="index.html">Home</a><a href="design-lab.html">Design Lab</a><a href="filmmaking.html">Filmmaking</a><a href="arts-studio.html">Arts Studio</a><a href="paintings.html">Paintings</a><a href="sculptures.html">Sculptures</a><a href="murals.html">Murals</a><a href="miniature-statues.html">Miniatures</a><a href="miniature-models.html">Models</a><a href="photography.html">Photography</a><a href="index.html#contact">Contact</a></nav>
      <span class="hand" style="font-size:1.1rem;color:#C9CBCF">Made by hand in Pune</span>
    </div>
    <span class="foot-plate"><img class="foot-logo" src="assets/logo/ziva-logo.png" alt="Ziva studio space"></span>
    <div class="foot-bottom"><span class="mono">© 2026 Ziva Studios</span><span class="mono">Design Lab · Filmmaking · Arts Studio</span></div>
  </div>
</footer>'''

LB = '''<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="close" type="button" aria-label="Close">✕</button>
  <figure><img alt=""></figure>
  <div class="bar"><span class="cap"></span><span class="nav-btns"><button class="prev" type="button" aria-label="Previous">←</button><button class="next" type="button" aria-label="Next">→</button></span></div>
</div>'''

BODIES = {
 'salon': '''<div class="wrap">
  <div class="filters" id="filters" role="group" aria-label="Filter paintings"></div>
  <div class="salon" id="gallery" data-layout="salon" data-filterable></div>
  <div class="section-label"><h2>In the studio</h2><span class="hand">Easel to wall, one frame at a time</span></div>
  <div class="strip" id="process"></div>
</div>''',
 'plinths': '''<div class="wrap">
  <div class="plinths" id="plinths"></div>
  <div class="filters" id="filters" role="group" aria-label="Filter sculptures"></div>
  <div class="tiles" id="gallery" data-layout="plinths" data-filterable></div>
</div>''',
 'hscroll': '''<section class="hs" id="gallery" data-layout="hscroll" aria-label="Murals, scroll to move sideways">
  <div class="hs-sticky"><div class="hs-track"></div><div class="hs-progress"><i></i></div></div>
</section>''',
 'shelf': '''<div class="wrap"><div class="shelf" id="gallery" data-layout="shelf"></div></div>''',
 'viewer': '''<div class="wrap">
  <div class="viewer" id="gallery" data-layout="viewer">
    <figure class="stage"><img alt=""><figcaption><span class="t"></span><span class="n mono"></span></figcaption></figure>
    <div class="thumbs" aria-label="Choose a view"></div>
  </div>
  <div class="specs">
    <div><span class="mono">Project</span>Temple hall interior</div>
    <div><span class="mono">Made of</span>Board, foam, resin and hand-painted panels</div>
    <div><span class="mono">Used for</span>Client presentation before the full build</div>
  </div>
</div>''',
 'atlas': '''<div class="wrap">
  <div class="atlas">
    <div class="map-wrap"><div id="map" role="region" aria-label="Map of Raigad district with numbered photo locations"></div><p class="map-note">Pins show approximate locations.</p></div>
    <div class="places" id="places"></div>
  </div>
  <div id="gallery" data-layout="atlas" hidden></div>
</div>''',
}

for slug, label, col, eyebrow, h1, lede, note, layout in PAGES:
    data = {'items': G[slug]}
    if slug == 'paintings': data['process'] = G['paintings-process']
    if slug == 'sculptures': data['featured'] = ['img-0574', 'shivaji-3', 'img-9316']
    others = ''.join(f'<a href="{s}.html">{l}</a>' for s, l, *_ in PAGES if s != slug)
    leaflet_css = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">' if layout == 'atlas' else ''
    leaflet_js = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>' if layout == 'atlas' else ''
    cover = G[slug][0]['lg']
    hl = ';--cad:var(--rose)' if col == '--rose' else ''
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(label)} · Ziva Studios</title>
<meta name="description" content="{e(lede)}">
<meta property="og:title" content="{e(label)} · Ziva Studios"><meta property="og:image" content="{cover}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rozha+One&family=Kalam:wght@400;700&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/site.css?v={VER}"><link rel="stylesheet" href="assets/gallery.css?v={VER}">{leaflet_css}
</head>
<body>
{nav(slug)}
<main>
<section class="page-hero">
  <div class="wrap">
    <div>
      <p class="crumbs mono">{'<a href="filmmaking.html">Filmmaking</a>' if slug == 'photography' else '<a href="arts-studio.html">Arts Studio</a>'}<span>/</span><span>{e(label)}</span></p>
      <h1>{e(h1.rsplit(" ",1)[0]+" ") if " " in h1 else ""}<span class="mark m-paint" style="{hl.lstrip(";")}">{e(h1.rsplit(" ",1)[-1])}</span></h1>
      <p class="lede">{e(lede)}</p>
    </div>
    <p class="note">{e(note)}</p>
  </div>
</section>
{BODIES[layout]}
<section class="cta-band">
  <div class="wrap">
    <div><h2>Want one of these?</h2><div class="other-pages">{others}</div></div>
    <a class="btn" href="index.html#contact">Start a project</a>
  </div>
</section>
</main>
{FOOT}
{LB}
<script>window.ZIVA={json.dumps(data, ensure_ascii=False, separators=(',', ':'))};</script>
{leaflet_js}
<script src="assets/gallery.js?v={VER}"></script>
</body>
</html>
'''
    (ROOT / f'{slug}.html').write_text(page, encoding='utf-8')
    print(slug, len(page))

# ---------------- Filmmaking division page (YouTube: Zindagi Vasool / Ziva Studios) ----------------
CHANNEL = 'https://www.youtube.com/@ZindagiVasoolOfficial'
UPLOADS = 'UUzfA9yjSwChmFiso-wsM-zw'   # channel's "all uploads" playlist
SERIES = [  # (playlist id, first video id, title, count, blurb)
 ('PLKOLJQ2cVvLFHC1rBDeKZXgMdlw-YNx3T', '-hd7CiFK3Rk', 'Zindagi Vasool with Saaku', 33, 'Travel, food and people, hosted by our creative director.'),
 ('PLKOLJQ2cVvLGga74droTXjV5XMBDjfzuy', 'rhEj7KKalng', 'Shivsparsh Vichar', 34, 'Long conversations on history, society and ideas.'),
 ('PLKOLJQ2cVvLE_wSZI4f2o6lm88PVLOXeh', 'dLjPt6Lbh3Y', 'पुरा-पर्यटन by Ketan Puri', 10, 'Caves, temples and lost cities of Maharashtra.'),
 ('PLKOLJQ2cVvLGh5gVbqiJDcl_82cUPduNj', 'WsJPHNblOww', 'Poems of Ziva Studios', 16, 'Marathi and Hindi poetry, shot as short films.'),
 ('PLKOLJQ2cVvLEurrM_GTu7oNDYfMHOJMfK', 'E3fBgM65fxo', 'प्रीतीसंगम काव्यकरंडक २०२५', 13, 'Recorded at the 2025 poetry competition.'),
 ('PLKOLJQ2cVvLH5kV-KDblqGKpUQbAjwf9K', 'QglMGJzaXXM', 'Dr. Swapnil Chaudhari Poems', 4, 'Poems on farmers, mothers and free speech.'),
 ('PLKOLJQ2cVvLE5pBHqKfldy5FpOVk4OJuc', 'E5peeh4Jn9M', 'Ziva Songs · Ajinkya Ankush', 2, 'Original music videos.'),
 ('PLKOLJQ2cVvLHaf5cHIT3yioJCmCAAsQCI', 'YxfSfAGcLGE', 'जगावेगळं Unconventional Stories', 1, 'A podcast of unusual lives.'),
]
SHORTS = [
 ('PLKOLJQ2cVvLGlqx_LXtRln87Q-60hDijl', 'aio7m7qz0QQ', 'Zindagi Vasool Shorts', 17),
 ('PLKOLJQ2cVvLFYMNmU5WJNcmqlOrKbnmAM', 'QZEluTagCnw', 'Shivsparsh Vichar Shorts', 12),
 ('PLKOLJQ2cVvLGMhhFXFvZNYmRUMQQa1-Y9', 'x6URucKXc9E', 'पुरा पर्यटन Shorts', 4),
 ('PLKOLJQ2cVvLFkkDwuo6OgP4p6e0Td0JZz', 'iFrwoxoMzOc', 'Journey-E-Dakkhan Shorts', 3),
 ('PLKOLJQ2cVvLGuBN-zZPNCR27tbLJbQOnx', 'dZ4y_2UKPc4', 'Travel Shorts', 1),
]
TOP = [  # most watched, linked to a channel search (views as of Nov 2026)
 ('Afzal Khan Vadh · Pramod Mande', '174K'), ('Nagraj Manjule Interview with Pradnyesh Molak', '141K'),
 ('Shivaji Maharaj यांची Paris येथील अस्सल चित्र', '116K'), ('कर्जबाजारपणाची जिंदगी by Swapnil Chaudhari', '96K'),
 ('शिवबा राजं छत्रपती झाला रं · Powada', '90K'), ('Sambal Solo Performance by Prasad Pawar', '16K'),
]
from urllib.parse import quote
def card(pl, vid, title, n, blurb='', cls='vcard'):
    return (f'<button class="{cls}" type="button" data-list="{pl}" aria-label="Play {e(title)}">'
            f'<span class="thumb"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy"><i class="play" aria-hidden="true"></i>'
            f'<b class="mono">{n} video{"s" if n != 1 else ""}</b></span><span class="vt">{e(title)}</span>'
            + (f'<span class="vb">{e(blurb)}</span>' if blurb else '') + '</button>')
film_body = f'''<div class="wrap">
  <div class="chips-row"><span>Ad films</span><span>Short films</span><span>Music videos</span><span>AV &amp; documentaries</span><span>Aerial cinematography</span></div>
  <div class="reel">
    <div class="player" id="player"><button class="poster" type="button" data-list="{UPLOADS}" aria-label="Play latest videos">
      <img src="https://i.ytimg.com/vi/-hd7CiFK3Rk/maxresdefault.jpg" alt="" onerror="this.onerror=null;this.src=this.src.replace('maxresdefault','hqdefault')"><i class="play big" aria-hidden="true"></i><span class="hand">Play our latest work</span></button></div>
    <aside class="channel">
      <span class="mono">Our channel</span><h2>Zindagi Vasool</h2>
      <p>Stories, interviews, travel and poetry in Marathi, made by the Ziva team since 2018.</p>
      <div class="stats"><div><b>12.4K</b><span class="mono">subscribers</span></div><div><b>204</b><span class="mono">videos</span></div></div>
      <a class="btn" href="{CHANNEL}" target="_blank" rel="noopener">Open on YouTube</a>
    </aside>
  </div>
  <div class="section-label"><h2>Series we make</h2><span class="hand">Tap one to play the whole playlist</span></div>
  <div class="vgrid">{"".join(card(*s) for s in SERIES)}</div>
  <div class="section-label"><h2>Shorts</h2><span class="hand">Vertical, under a minute</span></div>
  <div class="sgrid">{"".join(card(p, v, t, n, cls="vcard short") for p, v, t, n in SHORTS)}</div>
  <div class="section-label"><h2>Most watched</h2><span class="hand">Opens on YouTube</span></div>
  <ol class="top">{"".join(f'<li><a href="{CHANNEL}/search?query={quote(t)}" target="_blank" rel="noopener"><span>{e(t)}</span><b class="mono">{v} views</b></a></li>' for t, v in TOP)}</ol>
  <a class="photo-link" href="photography.html"><img src="{G['photography'][2]['sm']}" alt="" loading="lazy"><span><span class="mono">Also from this division</span><b>Photography: 30 places across Raigad</b></span></a>
  <div class="section-label"><h2>The film crew</h2></div>
  <div class="team crew">
    <div class="tag" style="--c:var(--rose);--fgc:#17181A"><header><b>HELLO</b><small>my name is</small></header><div class="nm">Pradnyesh Molak</div><p class="rl">Creative director, host & producer</p></div>
    <div class="tag" style="--c:var(--rose);--fgc:#17181A"><header><b>HELLO</b><small>my name is</small></header><div class="nm">Pankaj Lokhande</div><p class="rl">Director of photography & aerial drone operator</p></div>
    <div class="tag" style="--c:var(--ultra);--fgc:var(--on-ultra)"><header><b>HELLO</b><small>my name is</small></header><div class="nm">Manoj Janwekar</div><p class="rl">Editor & motion graphics</p></div>
  </div>
</div>'''
VM = '<div class="lb vm" id="vm" hidden role="dialog" aria-modal="true" aria-label="Video player"><button class="close" type="button" aria-label="Close">✕</button><div class="vbox"></div></div>'
FILM_JS = '''<script>
(function(){
  var vm=document.getElementById('vm'),box=vm.querySelector('.vbox');
  function src(l){return 'https://www.youtube-nocookie.com/embed/videoseries?list='+l+'&autoplay=1&rel=0'}
  function frame(l){return '<iframe src="'+src(l)+'" title="YouTube video player" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>'}
  document.querySelector('.poster').addEventListener('click',function(){document.getElementById('player').innerHTML=frame(this.dataset.list)});
  document.querySelectorAll('.vcard').forEach(function(b){b.addEventListener('click',function(){box.className='vbox'+(b.classList.contains('short')?' tall':'');box.innerHTML=frame(b.dataset.list);vm.hidden=false;document.body.style.overflow='hidden'})});
  function close(){vm.hidden=true;box.innerHTML='';document.body.style.overflow=''}
  vm.querySelector('.close').onclick=close;vm.addEventListener('click',function(e){if(e.target===vm)close()});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!vm.hidden)close()});
})();
</script>'''
fp = page  # reuse the last generated page as a shell: swap head, hero and body
import re
fp = re.sub(r'<title>.*?</title>', '<title>Filmmaking · Ziva Studios</title>', fp)
fp = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Ad films, short films, music videos, documentaries and aerial cinematography from Ziva Studios, Pune.">', fp)
fp = re.sub(r'<meta property="og:title".*?>', '<meta property="og:title" content="Filmmaking · Ziva Studios"><meta property="og:image" content="https://i.ytimg.com/vi/-hd7CiFK3Rk/maxresdefault.jpg">', fp)
fp = fp.replace('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">', '')
fp = fp.replace('<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>', '')
hero = '''<section class="page-hero">
  <div class="wrap">
    <div>
      <p class="crumbs mono"><a href="index.html#divisions">Divisions</a><span>/</span><span>Filmmaking</span></p>
      <h1><span class="mark m-paint" style="--cad:var(--rose)">Filmmaking</span></h1>
      <p class="lede">Ads, short films and songs, from script to drone shot to final grade. Most of what we shoot also lives on our own channel.</p>
    </div>
    <p class="note">Press play. Everything here was made by the same small team.</p>
  </div>
</section>'''
fp = re.sub(r'<section class="page-hero">.*?</section>', hero, fp, flags=re.S)
fp = re.sub(r'<div class="wrap">\n  <div class="atlas">.*?\n</div>\n(?=<section class="cta-band">)', film_body + '\n', fp, flags=re.S)
fp = fp.replace('<h2>Want one of these?</h2>', '<h2>Have a film in mind?</h2>')
fp = re.sub(r'<script>window\.ZIVA=.*?</script>\n', '', fp)
fp = fp.replace(f'<script src="assets/gallery.js?v={VER}"></script>', f'<script>window.ZIVA={{items:[]}};</script>\n<script src="assets/gallery.js?v={VER}"></script>\n' + FILM_JS)
fp = fp.replace('</footer>', '</footer>\n' + VM, 1)
fp = fp.replace('aria-current="page"', '')
(ROOT / 'filmmaking.html').write_text(fp, encoding='utf-8')
print('filmmaking', len(fp))

# ---------------- Design Lab and Arts Studio division pages ----------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rozha+One&family=Kalam:wght@400;700&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">')
def shell(slug, title, desc, og, crumb, h1, hl, lede, note, body, data, cta='Start a project'):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)} · Ziva Studios</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)} · Ziva Studios"><meta property="og:image" content="{og}">
{FONTS}
<link rel="stylesheet" href="assets/site.css?v={VER}"><link rel="stylesheet" href="assets/gallery.css?v={VER}">
</head>
<body>
{nav('')}
<main>
<section class="page-hero">
  <div class="wrap">
    <div>
      <p class="crumbs mono"><a href="index.html#divisions">Divisions</a><span>/</span><span>{e(crumb)}</span></p>
      <h1><span class="mark m-paint" style="{hl}">{e(h1)}</span></h1>
      <p class="lede">{e(lede)}</p>
    </div>
    <p class="note">{e(note)}</p>
  </div>
</section>
{body}
<section class="cta-band">
  <div class="wrap">
    <div><h2>Have something in mind?</h2><div class="other-pages"><a href="design-lab.html">Design Lab</a><a href="filmmaking.html">Filmmaking</a><a href="arts-studio.html">Arts Studio</a></div></div>
    <a class="btn" href="index.html#contact">{cta}</a>
  </div>
</section>
</main>
{FOOT}
{LB}
<script>window.ZIVA={json.dumps(data, ensure_ascii=False, separators=(',', ':'))};</script>
<script src="assets/gallery.js?v={VER}"></script>
</body>
</html>
'''
def figs(setname, items, cls='', cap=True, sizes='(max-width:700px) 46vw, 300px'):
    return ''.join(f'<figure class="g-item {cls}" data-set="{setname}" data-i="{i}" tabindex="0" role="button" aria-label="Open {e(x["title"])}">'
                   f'<img src="{x["sm"]}" srcset="{x["sm"]} 800w, {x["lg"]} 2400w" sizes="{sizes}" width="{x["w"]}" height="{x["h"]}" alt="{e(x["title"])}" loading="lazy" decoding="async">'
                   + (f'<figcaption>{e(x["title"])}</figcaption>' if cap else '') + '</figure>' for i, x in enumerate(items))
def tag(name, role, c, fg):
    return f'<div class="tag" style="--c:var({c});--fgc:{fg}"><header><b>HELLO</b><small>my name is</small></header><div class="nm">{name}</div><p class="rl">{role}</p></div>'
def chips(*xs): return '<div class="chips-row">' + ''.join(f'<span>{x}</span>' for x in xs) + '</div>'

# Design Lab
DV, MP, SV, LR = G['design-dataviz'], G['design-maps'], G['design-saheb'], G['design-letsread']
vids = [('media/maps/20.mp4', 'Mean maximum temperatures, 1970-2020'), ('media/maps/21.mp4', "India's export connections, 2022-23"),
        ('media/maps/22.mp4', 'Earthquakes of magnitude 5.5+, 2000-2020')]
dl_body = f'''<div class="wrap">
  {chips('Brand identity', 'Graphics &amp; social', 'Data visualisation', 'Infographics', 'Reports &amp; publications')}
  <div class="section-label" style="margin-top:0"><h2>Data visualisation</h2><span class="hand">{len(DV)} charts, each from a public dataset</span></div>
  <div class="pinboard">{figs('dv', DV)}</div>
  <div class="section-label"><h2>Maps</h2><span class="hand">QGIS, Python, Flourish and Datawrapper</span></div>
  <div class="mapgrid">{figs('mp', MP, sizes='(max-width:700px) 46vw, 260px')}
    {''.join(f'<figure class="vid"><video src="{v}" autoplay muted loop playsinline preload="metadata"></video><figcaption>{e(t)}</figcaption></figure>' for v, t in vids)}</div>
  <div class="section-label"><h2>Graphics &amp; social: Saheb Vishesh</h2><span class="hand">A 79-day Marathi post series. Drag or scroll →</span></div>
  <div class="strip deck">{figs('sv', SV, cap=False, sizes='340px')}</div>
  <div class="case">
    <div><span class="mono">Client</span><h2>Lets Read Foundation</h2><p>Infographics on India's public libraries, made in English and Marathi for the foundation's social channels.</p></div>
    <div class="case-imgs">{figs('lr', LR, cap=False, sizes='(max-width:700px) 46vw, 260px')}</div>
  </div>
  <div class="section-label"><h2>The lab team</h2></div>
  <div class="team crew">{tag('Manoj Janwekar', 'Editor, graphic designer & motion graphics', '--ultra', 'var(--on-ultra)')}{tag('Samruddhi Kadolkar', 'Graphic designer, illustrator & visual storyteller', '--sap', '#FBFBF8')}{tag('Vijay Jadhav', 'Data visualisation & infographics', '--ultra', 'var(--on-ultra)')}</div>
</div>'''
(ROOT / 'design-lab.html').write_text(shell('design-lab', 'Design Lab', 'Brand identity, graphics, data visualisation, maps and infographics from Ziva Studios, Pune.',
    DV[3]['lg'], 'Design Lab', 'Design Lab', '--cad:color-mix(in srgb, var(--ultra) 45%, var(--paper))',
    'Identity, graphics and data turned into something people can read at a glance. Charts, maps and social series, made from real data and checked twice.',
    'Every chart here started as a spreadsheet.', dl_body, {'items': [], 'dv': DV, 'mp': MP, 'sv': SV, 'lr': LR}), encoding='utf-8')

# Arts Studio
def pick(page, frag): return next(x for x in G[page] if frag in x['sm'])
tiles = [('paintings', 'Paintings', 'dsc00057'), ('sculptures', 'Sculptures', 'img-9316'), ('murals', 'Murals', 'img-0570'),
         ('miniature-statues', 'Miniature Statues', 'gb-3801'), ('miniature-models', 'Miniature Models', 'img-5573')]
tile_html = ''.join(f'<a class="atile" href="{s}.html"><img src="{pick(s, f)["sm"]}" srcset="{pick(s, f)["sm"]} 800w, {pick(s, f)["lg"]} 2400w" sizes="(max-width:700px) 92vw, 40vw" alt="" loading="lazy">'
                    f'<span><b>{t}</b><i class="mono">{len(G[s])} works →</i></span></a>' for s, t, f in tiles)
mats = [('100% linen canvas', 'Stretched over custom hardwood bars, the same cloth the old masters painted on.', pick('paintings-process', 'img-9579')),
        ('Old Master oil pigments', 'Handmade oils with the highest pigment load, so the colour stays true for centuries.', pick('paintings', 'modern-2')),
        ('Museum-grade glass & framing', 'Toughened glass and archival framing that shield the work from damp, dust and light.', pick('paintings', 'dsc00057')),
        ('Basalt stone', 'Sculpture in Deccan basalt, the stone of Maharashtra’s own forts and temples.', pick('sculptures', 'img-9993'))]
mat_html = ''.join(f'<figure class="mat-card"><img src="{x["sm"]}" alt="" loading="lazy"><figcaption><b>{t}</b><span>{d}</span></figcaption></figure>' for t, d, x in mats)
steps = [('Awareness', 'You see what we have made over the past decades, in halls, homes and public places.', pick('paintings', 'dsc00054')),
         ('Interest', 'We sit with you to understand the person, the place and the story the work should carry.', pick('paintings', 'makrand-dave')),
         ('Decision', 'Sketches, materials and a clear quotation. Work starts only when you approve.', pick('sculptures', '7135a56b')),
         ('Production', 'The master artist and assistants build it by hand, in oil, clay or stone.', pick('paintings-process', '174509')),
         ('Delivery & installation', 'Packed with care, delivered and installed by our own team.', pick('paintings', 'pan03584'))]
step_html = ''.join(f'<li><figure><img src="{x["sm"]}" alt="" loading="lazy"></figure><div><span class="mono">Step {i + 1}</span><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d, x) in enumerate(steps))
as_body = f'''<div class="wrap">
  {chips('Paintings', 'Murals', 'Sculptures', 'Miniature gifting', 'Scale models')}
  <div class="atiles">{tile_html}</div>
  <blockquote class="vision"><p>We create heirloom-grade paintings and sculpture, meticulously crafted to survive centuries, so a family’s legacy is not just remembered but physically present.</p>
    <p class="mono cite">Vision · Arts Studio</p></blockquote>
  <div class="ethos"><div><span class="mono">We do not mass-produce</span><p>We curate, consult and craft. Each piece is designed to stand the test of time, 500 years and beyond, with materials and techniques once reserved for royal portraits and temple masterpieces.</p></div></div>
  <div class="section-label"><h2>What makes our art last</h2><span class="hand">Four materials, no shortcuts</span></div>
  <div class="mats">{mat_html}</div>
  <div class="section-label"><h2>How a commission works</h2><span class="hand">Five steps, from first look to final wall</span></div>
  <ol class="journey">{step_html}</ol>
  <div class="section-label"><h2>What the price covers</h2></div>
  <div class="costs">
    <div><b>Archival materials</b><span>Premium art materials imported from makers with a long legacy.</span></div>
    <div><b>Master artist & assistants</b><span>Labour, research and brainstorming for every piece.</span></div>
    <div><b>Packaging & installation</b><span>Careful logistics, delivery and installation on site.</span></div>
  </div>
  <div class="section-label"><h2>In the studio</h2></div>
  <div class="team crew">{tag('Vishal Tajnekar', 'Painter & sculptor. JJ School of Arts', '--cad', '#17181A')}{tag('Pradnyesh Molak', 'Art curation & concepts', '--rose', '#17181A')}</div>
</div>'''
(ROOT / 'arts-studio.html').write_text(shell('arts-studio', 'Arts Studio', 'Heirloom paintings, sculpture in basalt and bronze, murals, miniatures and scale models from Ziva Studios, Pune.',
    pick('paintings', 'dsc00057')['lg'], 'Arts Studio', 'Arts Studio', '',
    'Paint, clay and stone. Ultra-premium paintings and sculpture made with archival materials and museum-level craft, to outlive the people who commission them.',
    'Made to last 500 years.', as_body, {'items': []}, cta='Commission a piece'), encoding='utf-8')
print('design-lab, arts-studio done')
