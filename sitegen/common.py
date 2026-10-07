# -*- coding: utf-8 -*-
"""Shared helpers for building the bilingual static site."""
import html as _html

SITE_NAME_EN = "Chengqi Xue"
SITE_NAME_ZH = "薛程琪"
EMAIL = "k25075983@kcl.ac.uk"
GITHUB = "https://github.com/Chengqi-Xue"


def t(en, zh):
    """Inline bilingual span pair."""
    return f'<span class="en">{en}</span><span class="zh">{zh}</span>'


def p(en, zh, cls=""):
    c = f' {cls}' if cls else ''
    return f'<p class="en{c}">{en}</p><p class="zh{c}">{zh}</p>'


def h(level, en, zh, cls="", id_=""):
    c = f' class="{cls}"' if cls else ''
    i = f' id="{id_}"' if id_ else ''
    return f'<h{level}{c}{i}>{t(en, zh)}</h{level}>'


def li(en, zh):
    return f'<li>{t(en, zh)}</li>'


def ul(items, cls=""):
    c = f' class="{cls}"' if cls else ''
    return f'<ul{c}>' + ''.join(li(e, z) for e, z in items) + '</ul>'


def figure(src, cap_en, cap_zh, cls="", alt="", wide=False, zoom=True):
    c = f' {cls}' if cls else ''
    w = ' fig-wide' if wide else ''
    z = ' data-zoom' if zoom else ''
    return (f'<figure class="fig{w}{c}"><img src="{src}" alt="{_html.escape(alt or cap_en)}" loading="lazy"{z}>'
            f'<figcaption>{t(cap_en, cap_zh)}</figcaption></figure>')


def figure_bi(src_en, src_zh, cap_en, cap_zh, cls="", alt="", wide=False):
    """Figure whose image itself has an EN and a ZH version."""
    c = f' {cls}' if cls else ''
    w = ' fig-wide' if wide else ''
    return (f'<figure class="fig{w}{c}"><img class="en" src="{src_en}" alt="{_html.escape(alt or cap_en)}" loading="lazy" data-zoom>'
            f'<img class="zh" src="{src_zh}" alt="{_html.escape(alt or cap_en)}" loading="lazy" data-zoom>'
            f'<figcaption>{t(cap_en, cap_zh)}</figcaption></figure>')


def video(src, poster, cap_en, cap_zh, cls="", wide=False, autoplay=False):
    c = f' {cls}' if cls else ''
    w = ' fig-wide' if wide else ''
    attrs = 'controls preload="metadata" playsinline'
    if autoplay:
        attrs = 'autoplay muted loop playsinline preload="metadata"'
    return (f'<figure class="fig vid{w}{c}"><video {attrs} poster="{poster}"><source src="{src}" type="video/mp4"></video>'
            f'<figcaption>{t(cap_en, cap_zh)}</figcaption></figure>')


def stats(items):
    """items: list of (value, label_en, label_zh)."""
    out = ['<div class="stats">']
    for v, e, z in items:
        out.append(f'<div class="stat"><div class="stat-v">{v}</div><div class="stat-l">{t(e, z)}</div></div>')
    out.append('</div>')
    return ''.join(out)


def steps(items):
    """Numbered process; items: list of (title_en, title_zh, body_en, body_zh)."""
    out = ['<ol class="steps">']
    for te, tz, be, bz in items:
        out.append(f'<li><div class="step-t">{t(te, tz)}</div><div class="step-b">{t(be, bz)}</div></li>')
    out.append('</ol>')
    return ''.join(out)


def section(id_, title_en, title_zh, body, lead_en=None, lead_zh=None, cls=""):
    c = f' {cls}' if cls else ''
    lead = p(lead_en, lead_zh, 'lead') if lead_en else ''
    return (f'<section class="sec{c}" id="{id_}"><div class="wrap">'
            f'<div class="sec-head">{h(2, title_en, title_zh)}{lead}</div>{body}</div></section>')


def head(title_en, title_zh, desc_en, root="", page_class=""):
    return f'''<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-en="{_html.escape(title_en)}" data-zh="{_html.escape(title_zh)}">{_html.escape(title_en)}</title>
<meta name="description" content="{_html.escape(desc_en)}">
<meta property="og:title" content="{_html.escape(title_en)}">
<meta property="og:description" content="{_html.escape(desc_en)}">
<meta property="og:image" content="https://chengqi-xue.github.io/assets/img/vtla-setup-overview.jpg">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
<script>(function(){{try{{var l=localStorage.getItem('lang');if(!l){{l=(navigator.language||'').toLowerCase().startsWith('zh')?'zh':'en';}}document.documentElement.setAttribute('data-lang',l);document.documentElement.lang=l==='zh'?'zh-CN':'en';}}catch(e){{}}}})();</script>
</head>
<body class="{page_class}">
'''


def header(root="", active=""):
    def nav(href, en, zh, key):
        a = ' aria-current="page"' if key == active else ''
        return f'<a href="{root}{href}"{a}>{t(en, zh)}</a>'
    return f'''<header class="top">
<div class="wrap top-in">
<a class="brand" href="{root}index.html"><span class="brand-zh">薛程琪</span><span class="brand-en">Chengqi Xue</span></a>
<nav class="nav">
{nav("index.html#research", "Research", "研究项目", "research")}
{nav("index.html#publications", "Publications", "论文与专利", "publications")}
{nav("index.html#about", "About", "关于我", "about")}
<a href="{root}assets/cv/Chengqi_Xue_CV_EN.pdf" class="en" target="_blank" rel="noopener">CV</a><a href="{root}assets/cv/Chengqi_Xue_CV_ZH.pdf" class="zh" target="_blank" rel="noopener">简历</a>
<button class="lang" type="button" id="langToggle" aria-label="Switch language"><span class="en">中文</span><span class="zh">English</span></button>
</nav>
<button class="menu-btn" type="button" id="menuBtn" aria-label="Menu" aria-expanded="false"><span></span><span></span></button>
</div>
</header>
'''


def footer(root=""):
    return f'''<footer class="foot">
<div class="wrap foot-in">
<div>
<div class="foot-name">薛程琪 · Chengqi Xue</div>
{p("MSc Robotics, King’s College London. Embodied intelligence and multimodal robot learning.", "伦敦国王学院机器人工程硕士，研究方向：具身智能与多模态机器人学习。")}
</div>
<div class="foot-links">
<a href="mailto:{EMAIL}">{EMAIL}</a>
<a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
<a href="https://scholar.google.com/scholar?q=Chengqi+Xue+PLOS+ONE" target="_blank" rel="noopener">Google Scholar</a>
<a href="{root}index.html#top">{t("Back to top", "回到顶部")}</a>
</div>
</div>
<div class="wrap foot-copy">© 2026 Chengqi Xue</div>
</footer>
<div class="lightbox" id="lightbox" hidden><button class="lb-close" aria-label="Close">×</button><img alt=""></div>
<script src="{root}assets/js/main.js"></script>
</body>
</html>
'''


def project_hero(index_label, title_en, title_zh, question_en, question_zh, meta, root="../"):
    """meta: list of (label_en, label_zh, value_en, value_zh)."""
    rows = ''.join(f'<div class="meta-row"><dt>{t(le, lz)}</dt><dd>{t(ve, vz)}</dd></div>' for le, lz, ve, vz in meta)
    return f'''<section class="phero">
<div class="wrap">
<a class="back" href="{root}index.html#research">{t("All research", "全部研究")}</a>
<div class="phero-grid">
<div>
<div class="phero-kind">{t(*index_label)}</div>
<h1>{t(title_en, title_zh)}</h1>
<p class="phero-q en">{question_en}</p><p class="phero-q zh">{question_zh}</p>
</div>
<dl class="meta">{rows}</dl>
</div>
</div>
</section>
'''


def links(items):
    """items: list of (href, label_en, label_zh)."""
    return '<div class="links">' + ''.join(
        f'<a class="btn" href="{href}" target="_blank" rel="noopener">{t(e, z)}</a>' for href, e, z in items) + '</div>'


def callout(en, zh, kind="note"):
    return f'<aside class="callout {kind}">{p(en, zh)}</aside>'


def two_col(left, right, cls=""):
    c = f' {cls}' if cls else ''
    return f'<div class="cols{c}"><div>{left}</div><div>{right}</div></div>'


def gallery(items, cols=3):
    """items: list of (src, cap_en, cap_zh)."""
    out = [f'<div class="gallery g{cols}">']
    for src, e, z in items:
        out.append(f'<figure class="fig"><img src="{src}" alt="{_html.escape(e)}" loading="lazy" data-zoom><figcaption>{t(e, z)}</figcaption></figure>')
    out.append('</div>')
    return ''.join(out)


def prose(*pairs):
    return ''.join(p(e, z) for e, z in pairs)
