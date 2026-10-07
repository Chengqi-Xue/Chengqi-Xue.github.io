(function () {
  'use strict';
  var root = document.documentElement;

  /* ---------- language toggle ---------- */
  function applyLang(l) {
    root.setAttribute('data-lang', l);
    root.lang = l === 'zh' ? 'zh-CN' : 'en';
    var tt = document.querySelector('title');
    if (tt && tt.dataset[l]) document.title = tt.dataset[l];
    try { localStorage.setItem('lang', l); } catch (e) {}
  }
  var btn = document.getElementById('langToggle');
  if (btn) btn.addEventListener('click', function () {
    applyLang(root.getAttribute('data-lang') === 'zh' ? 'en' : 'zh');
  });
  // set the document title for the initially chosen language
  (function () { var tt = document.querySelector('title'); var l = root.getAttribute('data-lang'); if (tt && tt.dataset[l]) document.title = tt.dataset[l]; })();

  /* ---------- mobile menu ---------- */
  var mb = document.getElementById('menuBtn'), nav = document.querySelector('.nav');
  if (mb && nav) mb.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    mb.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  /* ---------- lightbox ---------- */
  var lb = document.getElementById('lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    document.addEventListener('click', function (e) {
      var t = e.target;
      if (t.tagName === 'IMG' && t.hasAttribute('data-zoom')) {
        lbImg.src = t.currentSrc || t.src; lbImg.alt = t.alt || '';
        lb.hidden = false; document.body.style.overflow = 'hidden';
      } else if (!lb.hidden && (t === lb || t.classList.contains('lb-close') || t === lbImg)) {
        lb.hidden = true; document.body.style.overflow = '';
      }
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) { lb.hidden = true; document.body.style.overflow = ''; } });
  }

  /* ---------- hero: tactile marker field ----------
     A GelSight-like grid of markers. Moving the pointer "presses" the gel:
     markers near the pointer displace outward and the contact glows. */
  var cv = document.getElementById('gel');
  if (cv && cv.getContext) {
    var ctx = cv.getContext('2d');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var W, H, dpr, pts = [], gap = 34, px = -9999, py = -9999, tx = -9999, ty = -9999, raf, idle = 0;
    function build() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      pts = [];
      gap = W < 700 ? 28 : 34;
      for (var y = gap / 2; y < H + gap; y += gap) for (var x = gap / 2; x < W + gap; x += gap) pts.push({ x: x, y: y });
      draw();
    }
    function draw() {
      ctx.clearRect(0, 0, W, H);
      var R = Math.min(W, H) * 0.28, R2 = R * R;
      // contact glow
      if (px > -999) {
        var g = ctx.createRadialGradient(px, py, 0, px, py, R);
        g.addColorStop(0, 'rgba(28,158,138,0.28)'); g.addColorStop(0.55, 'rgba(222,106,146,0.10)'); g.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = g; ctx.fillRect(px - R, py - R, 2 * R, 2 * R);
      }
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i], dx = p.x - px, dy = p.y - py, d2 = dx * dx + dy * dy, ox = 0, oy = 0, a = 0.22, r = 1.6;
        if (d2 < R2) {
          var d = Math.sqrt(d2) || 1, k = 1 - d / R;        // 1 at centre, 0 at rim
          var push = k * k * gap * 0.9;                       // outward displacement
          ox = dx / d * push; oy = dy / d * push;
          a = 0.22 + k * 0.78; r = 1.6 + k * 1.9;
        }
        ctx.beginPath(); ctx.arc(p.x + ox, p.y + oy, r, 0, 6.2832);
        ctx.fillStyle = a > 0.6 ? 'rgba(170,240,225,' + a + ')' : 'rgba(245,247,246,' + a + ')';
        ctx.fill();
      }
    }
    function loop() {
      // ease the press point toward the pointer, like a gel settling
      px += (tx - px) * 0.18; py += (ty - py) * 0.18;
      draw();
      if (Math.abs(tx - px) + Math.abs(ty - py) > 0.3 || idle++ < 60) raf = requestAnimationFrame(loop); else raf = null;
    }
    function kick() { idle = 0; if (!raf) raf = requestAnimationFrame(loop); }
    function setTarget(x, y) {
      var b = cv.getBoundingClientRect(); tx = x - b.left; ty = y - b.top;
      if (px < -999) { px = tx; py = ty; }
      kick();
    }
    if (!reduce) {
      var hero = cv.parentElement;
      hero.addEventListener('mousemove', function (e) { setTarget(e.clientX, e.clientY); });
      hero.addEventListener('mouseleave', function () { tx = -9999; ty = -9999; kick(); });
      hero.addEventListener('touchmove', function (e) { var t = e.touches[0]; if (t) setTarget(t.clientX, t.clientY); }, { passive: true });
      hero.addEventListener('touchend', function () { tx = -9999; ty = -9999; kick(); });
      // an initial press so the idea is visible before anyone moves the pointer
      setTimeout(function () { if (px < -999) { var b = cv.getBoundingClientRect(); px = tx = b.width * 0.72; py = ty = b.height * 0.5; kick(); setTimeout(function () { if (Math.abs(tx - b.width * 0.72) < 1) { tx = -9999; ty = -9999; kick(); } }, 1800); } }, 600);
    }
    window.addEventListener('resize', build);
    build();
  }
})();
