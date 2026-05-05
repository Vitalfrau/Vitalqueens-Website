import json, os, re

with open(r'C:\Users\Andrea\Desktop\all_published_posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

CATEGORIES = {
    2335: ('koerperkompass', 'Körperkompass', 'cat-k'),
    2711: ('koerperkompass', 'Körperkompass', 'cat-k'),
    3254: ('koerperkompass', 'Körperkompass', 'cat-k'),
    3636: ('koerperkompass', 'Körperkompass', 'cat-k'),
    3845: ('koerperkompass', 'Körperkompass', 'cat-k'),
    4249: ('koerperkompass', 'Körperkompass', 'cat-k'),
    2421: ('female-business', 'Female Business', 'cat-b'),
    3249: ('female-business', 'Female Business', 'cat-b'),
    3924: ('female-business', 'Female Business', 'cat-b'),
    3977: ('female-business', 'Female Business', 'cat-b'),
    4161: ('female-business', 'Female Business', 'cat-b'),
    2373: ('persoenlich', 'Persönliches', 'cat-p'),
    2429: ('persoenlich', 'Persönliches', 'cat-p'),
    3099: ('persoenlich', 'Persönliches', 'cat-p'),
    3508: ('persoenlich', 'Persönliches', 'cat-p'),
    3697: ('persoenlich', 'Persönliches', 'cat-p'),
    3733: ('rezepte', 'Rezepte', 'cat-r'),
}

FREEBIE_FORM = '''
<div class="article-freebie">
  <div class="freebie-label">Kostenlos für dich</div>
  <h3 class="freebie-title">Hol dir deinen gratis Energieplan</h3>
  <p class="freebie-sub">Trag dich ein und erhalte deinen persönlichen Energieplan sofort per E-Mail.</p>
  <getresponse-form form-id="ef9fcc86-59ec-45d0-b999-c312c4c6ca1a" e="0"></getresponse-form>
</div>
'''

NAV = '''<nav id="mainNav">
  <a href="/index.html" class="nav-logo">Vital<span>Queens</span></a>
  <ul class="nav-links">
    <li><a href="/index.html">Start</a></li>
    <li class="nav-dropdown">
      <a href="/blog.html" class="nav-dropdown-trigger">Blog
        <svg class="nav-dropdown-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
      </a>
      <ul class="nav-dropdown-menu">
        <li><a href="/koerperkompass.html">Körperkompass</a></li>
        <li><a href="/female-business.html">Female Business</a></li>
        <li><a href="/persoenliches.html">Persönliches</a></li>
      </ul>
    </li>
    <li><a href="/rezepte.html">Rezepte</a></li>
    <li><a href="/index.html#ueber-mich">Über mich</a></li>
    <li><a href="/warteliste.html" class="nav-cta">Wartelistenplatz sichern</a></li>
    <li><a href="/newsletter.html">Newsletter</a></li>
    <li class="nav-divider"></li>
    <li><a href="/impressum.html" class="nav-legal-link">Impressum</a></li>
  </ul>
  <div class="nav-hamburger" id="hamburger" onclick="toggleMenu()">
    <span></span><span></span><span></span>
  </div>
</nav>'''

FOOTER = '''<footer>
  <div class="footer-top">
    <div class="footer-brand">
      <div class="footer-logo">Vital<span>Queens</span></div>
      <p class="footer-tagline">Achtsam wirken – Natürlich wachsen.<br>Energie &amp; Vitalität für Frauen 38+.</p>
    </div>
    <div class="footer-col">
      <h4>Themen</h4>
      <ul class="footer-links">
        <li><a href="/koerperkompass.html">Körperkompass</a></li>
        <li><a href="/female-business.html">Female Business</a></li>
        <li><a href="/persoenliches.html">Persönliches</a></li>
        <li><a href="/rezepte.html">Rezepte</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Community</h4>
      <ul class="footer-links">
        <li><a href="/newsletter.html">Newsletter</a></li>
        <li><a href="/warteliste.html">Warteliste</a></li>
        <li><a href="/index.html#ueber-mich">Über Andrea</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Für 0€</h4>
      <ul class="footer-links">
        <li><a href="/index.html#freebie">Energieplan</a></li>
        <li><a href="/newsletter.html">Newsletter</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p class="footer-copy">© 2026 VitalQueens · Alle Rechte vorbehalten</p>
    <div class="footer-legal">
      <a href="/impressum.html">Impressum</a>
      <a href="/datenschutz.html">Datenschutz</a>
    </div>
  </div>
</footer>'''

def clean_content(html):
    html = re.sub(r'<!-- /?wp:[^\-][^>]* ?/?-->', '', html)
    html = re.sub(r'\n{3,}', '\n\n', html)
    return html.strip()

def insert_freebie_midway(content, freebie):
    paras = re.findall(r'</p>', content)
    total = len(paras)
    if total < 4:
        return content + freebie
    mid = total // 2
    count = 0
    idx = 0
    while count < mid:
        pos = content.find('</p>', idx)
        if pos == -1:
            break
        idx = pos + 4
        count += 1
    return content[:idx] + freebie + content[idx:]

def make_article(post, cat_folder, cat_label, cat_class):
    title = post['post_title']
    date_raw = post['post_date'][:10]
    # Format date
    months = ['','Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
    y, m, d = date_raw.split('-')
    date_fmt = f"{int(d)}. {months[int(m)]} {y}"
    slug = post['post_name']
    raw_content = post['post_content']
    content = clean_content(raw_content)
    content_with_mid_form = insert_freebie_midway(content, FREEBIE_FORM)

    cat_colors = {
        'cat-k': '#3D8E9E',
        'cat-b': '#267060',
        'cat-p': '#5A4482',
        'cat-r': '#C4A255',
    }
    color = cat_colors.get(cat_class, '#3D8E9E')

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} – VitalQueens</title>
  <meta name="description" content="{title} – Lies den vollständigen Artikel auf VitalQueens.">
  <link rel="canonical" href="https://www.vitalqueens.de/{cat_folder}/{slug}.html">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --forest: #3D8E9E; --forest-mid: #4EA8B8;
      --gold: #C4A255; --gold-light: #D9BB78; --gold-pale: #F0E3C4;
      --cream: #F7F5F1; --cream-mid: #EBF2F0; --white: #FFFFFF;
      --ink: #22343C; --ink-soft: #446070; --ink-muted: #7298A6;
    }}
    html {{ scroll-behavior: smooth; }}
    body {{ font-family: 'Inter', sans-serif; background: var(--cream); color: var(--ink); overflow-x: hidden; -webkit-font-smoothing: antialiased; }}
    a {{ text-decoration: none; color: inherit; }}
    ul {{ list-style: none; }}
    img {{ display: block; max-width: 100%; }}
    nav {{ position: fixed; top: 0; left: 0; right: 0; z-index: 100; padding: 20px clamp(24px,5vw,80px); display: flex; align-items: center; justify-content: space-between; background: rgba(247,245,241,0.97); backdrop-filter: blur(20px); box-shadow: 0 1px 0 rgba(0,0,0,0.06); }}
    .nav-logo {{ font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: var(--forest); }}
    .nav-logo span {{ color: var(--gold); }}
    .nav-links {{ display: flex; gap: 22px; align-items: center; list-style: none; }}
    .nav-links a {{ font-size: 13px; font-weight: 500; color: var(--ink-soft); letter-spacing: 0.04em; transition: color 0.3s; position: relative; }}
    .nav-links a:hover {{ color: var(--forest); }}
    .nav-links a::after {{ content: ''; position: absolute; bottom: -3px; left: 0; right: 0; height: 1px; background: var(--gold); transform: scaleX(0); transform-origin: left; transition: transform 0.3s ease; }}
    .nav-links a:hover::after {{ transform: scaleX(1); }}
    .nav-cta {{ background: var(--forest); color: var(--cream) !important; padding: 10px 22px; border-radius: 100px; font-size: 13px !important; transition: background 0.3s !important; }}
    .nav-cta::after {{ display: none !important; }}
    .nav-cta:hover {{ background: var(--gold) !important; color: var(--forest) !important; }}
    .nav-divider {{ width: 1px; height: 16px; background: rgba(0,0,0,0.1); align-self: center; }}
    .nav-legal-link {{ font-size: 11px !important; color: var(--ink-muted) !important; }}
    .nav-dropdown {{ position: relative; }}
    .nav-dropdown-trigger {{ display: flex !important; align-items: center; gap: 4px; cursor: pointer; }}
    .nav-dropdown-trigger::after {{ display: none !important; }}
    .nav-dropdown-arrow {{ width: 11px; height: 11px; transition: transform 0.22s ease; }}
    .nav-dropdown:hover .nav-dropdown-arrow {{ transform: rotate(180deg); }}
    .nav-dropdown-menu {{ position: absolute; top: calc(100% + 16px); left: 50%; transform: translateX(-50%) translateY(-6px); background: var(--white); border-radius: 14px; box-shadow: 0 8px 40px rgba(34,52,60,0.13); padding: 10px 0; min-width: 200px; opacity: 0; visibility: hidden; transition: opacity 0.22s, transform 0.22s, visibility 0.22s; z-index: 200; border: 1px solid rgba(196,162,85,0.15); }}
    .nav-dropdown:hover .nav-dropdown-menu {{ opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0); }}
    .nav-dropdown-menu li {{ list-style: none; }}
    .nav-dropdown-menu a {{ display: block !important; padding: 10px 22px !important; font-size: 13px !important; color: var(--ink-soft) !important; white-space: nowrap; transition: background 0.15s, color 0.15s !important; }}
    .nav-dropdown-menu a::after {{ display: none !important; }}
    .nav-dropdown-menu a:hover {{ background: var(--cream-mid); color: var(--forest) !important; }}
    .nav-hamburger {{ display: none; flex-direction: column; gap: 5px; cursor: pointer; }}
    .nav-hamburger span {{ width: 24px; height: 1.5px; background: var(--forest); transition: all 0.3s; }}
    .article-hero {{ padding: 130px clamp(24px,5vw,80px) 60px; background: var(--forest); position: relative; overflow: hidden; }}
    .article-hero::before {{ content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 80% 50%, rgba(196,162,85,0.15) 0%, transparent 60%); }}
    .article-hero-inner {{ max-width: 800px; margin: 0 auto; position: relative; }}
    .article-cat {{ display: inline-block; font-size: 11px; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; background: rgba(255,255,255,0.15); color: var(--gold-light); padding: 5px 14px; border-radius: 20px; margin-bottom: 20px; }}
    .article-hero h1 {{ font-family: 'Playfair Display', serif; font-size: clamp(28px,4vw,52px); font-weight: 700; color: var(--white); line-height: 1.15; margin-bottom: 20px; }}
    .article-meta {{ font-size: 13px; color: rgba(255,255,255,0.55); }}
    .article-body {{ max-width: 780px; margin: 0 auto; padding: clamp(48px,7vw,90px) clamp(24px,5vw,40px); }}
    .article-body h2 {{ font-family: 'Playfair Display', serif; font-size: clamp(22px,2.8vw,34px); font-weight: 700; color: var(--ink); margin: 48px 0 18px; line-height: 1.2; }}
    .article-body h3 {{ font-family: 'Playfair Display', serif; font-size: clamp(18px,2vw,26px); font-weight: 700; color: var(--ink); margin: 36px 0 14px; }}
    .article-body h4, .article-body h5 {{ font-family: 'Inter', sans-serif; font-size: 16px; font-weight: 600; color: var(--ink); margin: 28px 0 10px; }}
    .article-body p {{ font-size: 17px; line-height: 1.8; color: var(--ink-soft); margin-bottom: 22px; }}
    .article-body ul, .article-body ol {{ margin: 0 0 22px 24px; }}
    .article-body li {{ font-size: 16px; line-height: 1.75; color: var(--ink-soft); margin-bottom: 8px; }}
    .article-body ul {{ list-style: disc; }}
    .article-body ol {{ list-style: decimal; }}
    .article-body strong {{ color: var(--ink); font-weight: 600; }}
    .article-body em {{ font-style: italic; }}
    .article-body blockquote {{ border-left: 3px solid var(--gold); padding: 16px 24px; margin: 32px 0; background: var(--gold-pale); border-radius: 0 12px 12px 0; font-style: italic; color: var(--ink); }}
    .article-body hr {{ border: none; border-top: 1px solid rgba(34,52,60,0.1); margin: 40px 0; }}
    .article-freebie {{ background: var(--cream-mid); border: 1px solid rgba(196,162,85,0.25); border-radius: 20px; padding: 36px; margin: 48px 0; text-align: center; }}
    .freebie-label {{ font-size: 11px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--gold); margin-bottom: 12px; }}
    .freebie-title {{ font-family: 'Playfair Display', serif; font-size: clamp(20px,2.5vw,28px); font-weight: 700; color: var(--ink); margin-bottom: 10px; }}
    .freebie-sub {{ font-size: 15px; color: var(--ink-muted); margin-bottom: 20px; }}
    .article-back {{ display: inline-flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: var(--forest); margin-bottom: 48px; transition: gap 0.2s; }}
    .article-back:hover {{ gap: 12px; }}
    footer {{ background: var(--forest); color: var(--white); padding: clamp(60px,8vw,100px) clamp(24px,5vw,80px) 0; }}
    .footer-top {{ display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; padding-bottom: 60px; border-bottom: 1px solid rgba(255,255,255,0.1); }}
    .footer-logo {{ font-family: 'Playfair Display', serif; font-size: 24px; font-weight: 700; margin-bottom: 12px; }}
    .footer-logo span {{ color: var(--gold); }}
    .footer-tagline {{ font-size: 14px; color: rgba(255,255,255,0.5); line-height: 1.6; }}
    .footer-col h4 {{ font-size: 11px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: rgba(255,255,255,0.4); margin-bottom: 20px; }}
    .footer-links {{ list-style: none; }}
    .footer-links a {{ display: block; padding: 5px 0; font-size: 14px; color: rgba(255,255,255,0.6); transition: color 0.2s; }}
    .footer-links a:hover {{ color: var(--white); }}
    .footer-bottom {{ display: flex; justify-content: space-between; align-items: center; padding: 24px 0; border-top: 1px solid rgba(255,255,255,0.08); margin-top: 8px; flex-wrap: wrap; gap: 12px; }}
    .footer-copy {{ font-size: 13px; color: rgba(255,255,255,0.3); }}
    .footer-legal {{ display: flex; gap: 24px; }}
    .footer-legal a {{ font-size: 13px; color: rgba(255,255,255,0.3); transition: color 0.2s; }}
    .footer-legal a:hover {{ color: rgba(255,255,255,0.7); }}
    .nav-mobile-open .nav-links {{ display: flex !important; flex-direction: column; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: var(--cream); z-index: 99; justify-content: center; align-items: center; gap: 32px; }}
    @media (max-width: 900px) {{ .footer-top {{ grid-template-columns: 1fr 1fr; }} }}
    @media (max-width: 600px) {{ .nav-links {{ display: none; }} .nav-hamburger {{ display: flex; }} .footer-top {{ grid-template-columns: 1fr; }} .footer-bottom {{ flex-direction: column; text-align: center; }} }}
  </style>
</head>
<body>
{NAV}

<section class="article-hero">
  <div class="article-hero-inner">
    <span class="article-cat">{cat_label}</span>
    <h1>{title}</h1>
    <p class="article-meta">{date_fmt}</p>
  </div>
</section>

<main class="article-body">
  <a href="/{cat_folder}.html" class="article-back">← Zurück zu {cat_label}</a>
  {content_with_mid_form}
  {FREEBIE_FORM}
</main>

{FOOTER}

<script>
function toggleMenu() {{ document.body.classList.toggle('nav-mobile-open'); }}
</script>
<script async src="https://app.getresponse.com/static/plugins/webform-plugin/webform.js"></script>
</body>
</html>'''

BASE = r'C:\Users\Andrea\Desktop\Claude Ordner\Vitalqueens'

for post in posts:
    pid = int(post['id'])
    if pid not in CATEGORIES:
        continue
    cat_folder, cat_label, cat_class = CATEGORIES[pid]
    folder = os.path.join(BASE, cat_folder)
    os.makedirs(folder, exist_ok=True)
    slug = post['post_name']
    html = make_article(post, cat_folder, cat_label, cat_class)
    path = os.path.join(folder, f'{slug}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Created: {cat_folder}/{slug}.html')

print('Done!')
