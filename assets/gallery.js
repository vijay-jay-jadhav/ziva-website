/* Category pages: nav, theme, lightbox and one renderer per layout. Data comes from window.ZIVA (inlined by tools/build_pages.py). */
(function () {
  var D = window.ZIVA || {}, items = D.items || [], root = document.documentElement;

  // nav + theme (same behaviour as the home page)
  var menuBtn = document.getElementById('menuBtn'), links = document.getElementById('links');
  menuBtn.addEventListener('click', function () { var o = links.classList.toggle('open'); menuBtn.setAttribute('aria-expanded', o) });
  var tb = document.getElementById('themeBtn');
  function isDark() { var t = root.getAttribute('data-theme'); return t ? t === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches }
  try { var saved = localStorage.getItem('ziva-theme'); if (saved) root.setAttribute('data-theme', saved) } catch (e) {}
  tb.addEventListener('click', function () { var n = isDark() ? 'light' : 'dark'; root.setAttribute('data-theme', n); try { localStorage.setItem('ziva-theme', n) } catch (e) {} });

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] }) }
  function img(x, sizes, extra) {
    return '<img src="' + x.sm + '" srcset="' + x.sm + ' 800w, ' + x.lg + ' 2400w" sizes="' + (sizes || '33vw') + '" width="' + x.w + '" height="' + x.h +
      '" alt="' + esc(x.title) + '" loading="lazy" decoding="async"' + (extra || '') + '>';
  }
  function fig(x, i, cls, cap, sizes) {
    return '<figure class="g-item ' + (cls || '') + '" data-i="' + i + '" data-group="' + esc(x.group) + '" tabindex="0" role="button" aria-label="Open ' + esc(x.title) + '">' +
      img(x, sizes) + (cap || '') + '</figure>';
  }

  // ---------- lightbox ----------
  var lb = document.getElementById('lb'), lbImg = lb.querySelector('img'), lbCap = lb.querySelector('.cap'), list = items, cur = 0, lastFocus;
  function show(i) {
    cur = (i + list.length) % list.length; var x = list[cur];
    lbImg.src = x.lg; lbImg.alt = x.title;
    lbCap.innerHTML = esc(x.title) + '<small>' + esc(x.group) + ' · ' + (cur + 1) + ' / ' + list.length + '</small>';
    var n = list[(cur + 1) % list.length]; (new Image()).src = n.lg;
  }
  function open(i, set) { list = set || items; lastFocus = document.activeElement; show(i); lb.hidden = false; document.body.style.overflow = 'hidden'; lb.querySelector('.close').focus() }
  function close() { lb.hidden = true; document.body.style.overflow = ''; if (lastFocus) lastFocus.focus() }
  lb.querySelector('.close').onclick = close;
  lb.querySelector('.prev').onclick = function () { show(cur - 1) };
  lb.querySelector('.next').onclick = function () { show(cur + 1) };
  lb.addEventListener('click', function (e) { if (e.target === lb || e.target.tagName === 'FIGURE') close() });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') show(cur + 1); if (e.key === 'ArrowLeft') show(cur - 1);
  });
  var sx = null;
  lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX }, { passive: true });
  lb.addEventListener('touchend', function (e) { if (sx == null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); sx = null });

  // any .g-item opens the lightbox for its own set (data-set) or the page set
  document.addEventListener('click', function (e) {
    var f = e.target.closest('.g-item'); if (!f) return;
    var set = f.dataset.set === 'process' ? D.process : visible();
    var x = (f.dataset.set === 'process' ? D.process : items)[+f.dataset.i];
    open(set.indexOf(x), set);
  });
  document.addEventListener('keydown', function (e) { if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('g-item')) { e.preventDefault(); e.target.click() } });

  // filters (paintings, sculptures)
  var active = 'All';
  function visible() { return active === 'All' ? items : items.filter(function (x) { return x.group === active }) }
  function filters(el) {
    if (!el) return;
    var groups = ['All'].concat(items.map(function (x) { return x.group }).filter(function (g, i, a) { return a.indexOf(g) === i }));
    el.innerHTML = groups.map(function (g) {
      var n = g === 'All' ? items.length : items.filter(function (x) { return x.group === g }).length;
      return '<button type="button" aria-pressed="' + (g === 'All') + '" data-g="' + esc(g) + '">' + esc(g) + '<span class="count">' + n + '</span></button>';
    }).join('');
    el.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return; active = b.dataset.g;
      el.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b) });
      document.querySelectorAll('[data-filterable] .g-item').forEach(function (f) { f.hidden = active !== 'All' && f.dataset.group !== active });
    });
  }

  var G = document.getElementById('gallery'); if (!G) return; var layout = G.dataset.layout;

  if (layout === 'salon') {
    filters(document.getElementById('filters'));
    G.innerHTML = items.map(function (x, i) {
      return fig(x, i, '', '', '(max-width:700px) 92vw, 30vw').replace('<img', '<div class="frame"><div class="mat"><img').replace(/(<img[^>]*>)/, '$1</div></div>')
        .replace('</figure>', '<figcaption><span>' + esc(x.title) + '</span><span class="mono">' + esc(x.group) + '</span></figcaption></figure>');
    }).join('');
    var P = document.getElementById('process');
    if (P && D.process) P.innerHTML = D.process.map(function (x, i) {
      return fig(x, i, '', '<figcaption>' + esc(x.title) + '</figcaption>', '320px').replace('class="g-item ', 'data-set="process" class="g-item ');
    }).join('');
  }

  if (layout === 'plinths') {
    filters(document.getElementById('filters'));
    var feat = (D.featured || []).map(function (k) { return items.findIndex(function (x) { return x.sm.indexOf(k) > -1 }) });
    document.getElementById('plinths').innerHTML = feat.map(function (i) {
      return '<div class="plinth">' + fig(items[i], i, '', '', '(max-width:700px) 46vw, 30vw') + '<div class="base"><span>' + esc(items[i].title) + '</span></div></div>';
    }).join('');
    G.innerHTML = items.map(function (x, i) { return fig(x, i, '', '<figcaption>' + esc(x.title) + '</figcaption>', '(max-width:700px) 46vw, 240px') }).join('');
  }

  if (layout === 'hscroll') {
    var html = '', last = '', ch = 0;
    items.forEach(function (x, i) {
      if (x.group !== last) { last = x.group; var n = items.filter(function (y) { return y.group === x.group }).length;
        html += '<div class="chapter"><span class="mono">Project ' + String(++ch).padStart(2, '0') + '</span><h2>' + esc(x.group) +
          '</h2><span class="hand">' + n + ' photos · scroll on →</span></div>' }
      html += fig(x, i, '', '<figcaption>' + esc(x.title) + '</figcaption>', '60vh');
    });
    var track = G.querySelector('.hs-track'); track.innerHTML = html;
    var sec = G, bar = G.querySelector('.hs-progress i'), mq = matchMedia('(min-width:861px) and (prefers-reduced-motion:no-preference)'), dist = 0;
    function measure() { if (!mq.matches) { sec.style.height = ''; return } dist = Math.max(0, track.scrollWidth - innerWidth); sec.style.height = (dist + innerHeight) + 'px'; tick() }
    function tick() {
      if (!mq.matches) return; var r = sec.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / Math.max(1, dist)));
      track.style.transform = 'translateX(' + (-p * dist) + 'px)'; bar.style.width = (p * 100) + '%';
    }
    addEventListener('scroll', function () { requestAnimationFrame(tick) }, { passive: true });
    addEventListener('resize', measure); addEventListener('load', measure); measure();
    track.querySelectorAll('img').forEach(function (im) { im.addEventListener('load', measure) });
  }

  if (layout === 'shelf') {
    G.innerHTML = items.map(function (x, i) {
      return '<article class="product">' + fig(x, i, '', '', '(max-width:600px) 92vw, 300px') + '<div class="info"><h3>' + esc(x.title) +
        '</h3><a class="ask" href="index.html#contact">Enquire</a></div></article>';
    }).join('');
  }

  if (layout === 'viewer') {
    var st = G.querySelector('.stage img'), cap = G.querySelector('.stage .t'), num = G.querySelector('.stage .n'), th = G.querySelector('.thumbs');
    th.innerHTML = items.map(function (x, i) { return '<button type="button" data-i="' + i + '" aria-label="' + esc(x.title) + '">' + img(x, '120px') + '</button>' }).join('');
    function pick(i) {
      var x = items[i]; st.src = x.lg; st.srcset = x.sm + ' 800w, ' + x.lg + ' 2400w'; st.alt = x.title; st.dataset.i = i;
      cap.textContent = x.title; num.textContent = (i + 1) + ' / ' + items.length;
      th.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-current', +b.dataset.i === i) });
    }
    th.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) pick(+b.dataset.i) });
    st.addEventListener('click', function () { open(+st.dataset.i, items) });
    pick(0);
  }

  if (layout === 'atlas') {
    var P = document.getElementById('places');
    P.innerHTML = items.map(function (x, i) {
      return '<button class="place" type="button" data-i="' + i + '">' + img(x, '(max-width:900px) 46vw, 240px') + '<span><b>' + String(i + 1).padStart(2, '0') + '</b>' + esc(x.title) + '</span></button>';
    }).join('');
    var markers = [];
    function hi(i, on) { var b = P.children[i]; if (b) b.classList.toggle('on', on); if (markers[i]) markers[i].getElement() && markers[i].getElement().classList.toggle('on', on) }
    P.addEventListener('click', function (e) { var b = e.target.closest('.place'); if (b) open(+b.dataset.i, items) });
    P.addEventListener('mouseover', function (e) { var b = e.target.closest('.place'); if (b) { hi(+b.dataset.i, true); if (window.zmap) zmap.panTo(markers[+b.dataset.i].getLatLng()) } });
    P.addEventListener('mouseout', function (e) { var b = e.target.closest('.place'); if (b) hi(+b.dataset.i, false) });
    if (window.L) {
      var zmap = window.zmap = L.map('map', { scrollWheelZoom: false }).setView([18.45, 73.15], 9);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO', maxZoom: 16 }).addTo(zmap);
      items.forEach(function (x, i) {
        var m = L.marker([x.lat, x.lon], { icon: L.divIcon({ className: 'pin-num', html: String(i + 1), iconSize: [26, 26] }), title: x.title, keyboard: true }).addTo(zmap);
        m.on('click', function () { open(i, items) });
        m.on('mouseover', function () { hi(i, true); P.children[i].scrollIntoView({ block: 'nearest', behavior: 'smooth' }) });
        m.on('mouseout', function () { hi(i, false) });
        markers.push(m);
      });
      zmap.fitBounds(L.latLngBounds(items.map(function (x) { return [x.lat, x.lon] })), { padding: [30, 30] });
    } else document.getElementById('map').innerHTML = '<p style="padding:20px">Map could not load. The photos are listed alongside.</p>';
  }
})();
