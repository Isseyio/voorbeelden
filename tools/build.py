#!/usr/bin/env python3
"""Bouwt per merk een voorbeeldpagina uit brands/<slug>.json.

Gebruik:
  python3 tools/build.py            # alle merken
  python3 tools/build.py <slug>     # één merk

Per merk:
  brands/<slug>.json      gegevens (zie brands/_voorbeeld.json)
  <slug>/src/*.png        exports uit Figma (ad1.png … adN.png, mail.png), 2x
Resultaat:
  <slug>/index.html, <slug>/img/*.webp, <slug>/img/og.jpg
De map src/ wordt niet gepubliceerd (staat in .gitignore).
"""
import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://voorbeelden.digitalessence.io"
CONTACT = {
    "naam": "Issey Kooijmans",
    "rol": "Founder Digital Essence",
    "plaats": "Utrecht",
    "email": "issey@digitalessence.io",
    "tel": "+31643003935",
    "tel_label": "+31 6 43003935",
    "whatsapp": "31643003935",
    "meet": "https://calendar.app.google/CyLvHxXww7ogm8699",
    "site": "https://digitalessence.io",
    "linkedin": "https://www.linkedin.com/in/isseyk",
}
WEEK = [
    ("Ma", "Nieuwe advertenties live", "Verschillende invalshoeken tegelijk testen."),
    ("Di", "Meekijken", "Wat pakt de doelgroep op, wat niet?"),
    ("Wo", "Bijsturen", "Budget naar wat werkt, de rest eruit."),
    ("Do", "Nieuwsbrief verstuurd", "Vast moment, zodat lezers erop gaan rekenen."),
    ("Vr", "Korte update", "Wat werkte en wat we volgende week doen."),
]


def esc(s):
    return html.escape(str(s or ""), quote=True)


def webp(src: Path, dst: Path, width: int, quality: int = 82):
    im = Image.open(src).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=quality, method=6)
    return im.size


def og_image(ads, dst: Path, bg="#F2F2F4"):
    W, H = 1200, 630
    c = Image.new("RGB", (W, H), bg)
    pick = ads[:3]
    h = 540
    w = round(h * 9 / 16)
    gap = 36
    total = len(pick) * w + (len(pick) - 1) * gap
    x = (W - total) // 2
    for p in pick:
        im = Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS)
        mask = Image.new("L", (w, h), 0)
        from PIL import ImageDraw
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius=22, fill=255)
        c.paste(im, (x, (H - h) // 2), mask)
        x += w + gap
    c.save(dst, "JPEG", quality=84, optimize=True)


def build(slug: str):
    data = json.loads((ROOT / "brands" / f"{slug}.json").read_text("utf-8"))
    brand = data["merk"]
    page = ROOT / slug
    src = page / "src"
    img = page / "img"
    img.mkdir(parents=True, exist_ok=True)

    ads = data["advertenties"]
    ad_srcs = []
    for i, ad in enumerate(ads, 1):
        s = src / ad["bestand"]
        ad_srcs.append(s)
        webp(s, img / f"ad{i}.webp", 1080)
        webp(s, img / f"ad{i}-s.webp", 540, 80)
    mail = data.get("nieuwsbrief")
    mail_size = None
    if mail:
        mail_size = webp(src / mail["bestand"], img / "mail.webp", 1200, 80)
    og_image(ad_srcs, img / "og.jpg")

    accent = data.get("accent", "#111111")
    n = len(ads)
    telwoord = {1: "Eén", 2: "Twee", 3: "Drie", 4: "Vier", 5: "Vijf", 6: "Zes", 7: "Zeven", 8: "Acht"}.get(n, str(n))
    title = f"Voorbeelden voor {brand}"
    intro = data.get("intro") or (
        f"{telwoord} advertenties{' en een nieuwsbrief' if mail else ''}, gemaakt met jullie eigen foto's en productinformatie."
    )
    wa_text = quote(f"Hoi Issey, ik heb de voorbeelden voor {brand} gezien.")
    mail_subject = quote(f"Voorbeelden voor {brand}")

    cards = []
    for i, ad in enumerate(ads, 1):
        cards.append(f"""
      <li class="ad">
        <button class="ad-btn" data-i="{i-1}" aria-label="Bekijk advertentie {i} groot">
          <img src="img/ad{i}-s.webp" srcset="img/ad{i}-s.webp 540w, img/ad{i}.webp 1080w" sizes="(min-width: 1100px) 210px, (min-width: 700px) 30vw, 70vw" width="540" height="960" alt="Advertentie {i} voor {esc(brand)}: {esc(ad['titel'])}" loading="{'eager' if i <= 2 else 'lazy'}" decoding="async">
        </button>
        <div class="ad-meta">
          <span class="ad-n">{i:02d}</span>
          <h3>{esc(ad['titel'])}</h3>
          <p>{esc(ad.get('waarom', ''))}</p>
        </div>
      </li>""")

    lb = "".join(
        f'<figure class="lb-slide"><img src="img/ad{i}.webp" width="1080" height="1920" alt="Advertentie {i}: {esc(ad["titel"])}" loading="lazy" decoding="async"><figcaption>{i:02d} · {esc(ad["titel"])}</figcaption></figure>'
        for i, ad in enumerate(ads, 1)
    )

    fan_idx = [1, 0, 2] if n >= 3 else list(range(n))
    fan = "".join(f'<img src="img/ad{j+1}-s.webp" width="540" height="960" alt="" decoding="async">' for j in fan_idx)

    mail_html = ""
    if mail:
        mw, mh = mail_size
        punten = "".join(f"<li>{esc(p)}</li>" for p in mail.get("punten", []))
        mail_html = f"""
  <section class="sec mail-sec" id="nieuwsbrief">
    <div class="wrap mail-grid">
      <div class="mail-copy">
        <p class="eyebrow">Nieuwsbrief</p>
        <h2>{esc(mail.get('kop') or 'Een nieuwsbrief in jullie eigen stijl.')}</h2>
        <p class="lead">{esc(mail.get('tekst') or 'Met jullie lettertypes, kleuren en knoppen, zodat hij voelt als jullie eigen mail.')}</p>
        {f'<ul class="ticks">{punten}</ul>' if punten else ''}
      </div>
      <div class="mail-frame">
        <div class="mail-head">
          <div class="mail-av" style="background:{esc(accent)}">{esc(brand[:1])}</div>
          <div class="mail-from">
            <strong>{esc(brand)}</strong>
            <span>{esc(mail.get('onderwerp', ''))}</span>
          </div>
        </div>
        <div class="mail-body"><img src="img/mail.webp" width="{mw}" height="{mh}" alt="Voorbeeldnieuwsbrief voor {esc(brand)}" loading="lazy" decoding="async"></div>
        <button class="mail-more" type="button">Lees de hele nieuwsbrief</button>
      </div>
    </div>
  </section>"""

    week = "".join(
        f'<li><span class="day">{d}</span><strong>{esc(t)}</strong><span class="sub">{esc(s)}</span></li>'
        for d, t, s in WEEK
    )

    ai_line = "Sfeerbeelden zijn deels met AI gemaakt; de producten zijn jullie eigen productfoto's. " if data.get("ai_sfeer") else ""
    photo = (ROOT / "assets" / "issey.jpg").exists()
    avatar = (
        '<img class="me-photo" src="../assets/issey.jpg" width="96" height="96" alt="Issey Kooijmans">'
        if photo
        else '<div class="me-photo me-mono" aria-hidden="true">IK</div>'
    )

    out = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>{esc(title)} · Digital Essence</title>
<meta name="description" content="{esc(intro)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(intro)}">
<meta property="og:image" content="{BASE_URL}/{slug}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{BASE_URL}/{slug}/">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5F5F7">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css?v=3">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<style>:root{{--brand:{esc(accent)}}}</style>
</head>
<body>
<header class="top">
  <div class="wrap top-in">
    <a class="logo" href="{CONTACT['site']}" aria-label="Digital Essence">Digital Essence</a>
    <a class="pill pill-wa" href="https://wa.me/{CONTACT['whatsapp']}?text={wa_text}">WhatsApp</a>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
      <p class="eyebrow"><span class="dot"></span>Voorbeelden voor {esc(brand)}</p>
      <h1>{esc(data.get('kop') or f'Zo kunnen de advertenties van {brand} eruitzien.')}</h1>
      <p class="lead">{esc(intro)} Een idee van {CONTACT['naam']} van Digital Essence; niets hiervan is gepubliceerd.</p>
      <div class="hero-cta">
        <a class="btn btn-dark" href="#advertenties">Bekijk de voorbeelden</a>
        <a class="btn btn-ghost" href="#contact">Even sparren?</a>
      </div>
      </div>
      <div class="fan" aria-hidden="true">{fan}</div>
    </div>
  </section>

  <section class="sec" id="advertenties">
    <div class="wrap">
      <div class="sec-head">
        <div>
          <p class="eyebrow">Advertenties · 9:16</p>
          <h2>{telwoord} invalshoeken om te testen.</h2>
        </div>
        <p class="hint">Tik op een advertentie om hem groot te bekijken.</p>
      </div>
    </div>
    <ul class="ads" role="list">{''.join(cards)}
    </ul>
  </section>
{mail_html}
  <section class="sec week-sec">
    <div class="wrap">
      <p class="eyebrow">Ritme</p>
      <h2>Zo kan een week eruitzien.</h2>
      <p class="lead">Dit is een voorbeeld, geen vast pakket. De kracht zit in het ritme: regelmatig nieuwe advertenties testen en je nieuwsbrief vast versturen. Wat werkt, doen we vaker.</p>
      <ol class="week">{week}</ol>
      <div class="facts">
        <div><strong>Advertenties</strong><span>zoveel als bij jullie past</span></div>
        <div><strong>Nieuwsbrief</strong><span>per week, of vaker als dat beter werkt</span></div>
        <div><strong>Vrij</strong><span>per week, per maand of per campagne</span></div>
      </div>
    </div>
  </section>

  <section class="sec contact-sec" id="contact">
    <div class="wrap">
      <div class="contact-card">
        <div class="me">
          {avatar}
          <div>
            <strong>{CONTACT['naam']}</strong>
            <span>{CONTACT['rol']} · {CONTACT['plaats']}</span>
          </div>
        </div>
        <h2>Benieuwd hoe dit voor {esc(brand)} werkt?</h2>
        <p class="lead">Een kwartiertje bellen is genoeg om te kijken of het past. Geen verplichtingen.</p>
        <div class="cta-stack">
          <a class="btn btn-wa" href="https://wa.me/{CONTACT['whatsapp']}?text={wa_text}">Stuur me een WhatsApp</a>
          <a class="btn btn-meet" href="{CONTACT['meet']}">Plan een videogesprek</a>
          <a class="btn btn-ghost" href="mailto:{CONTACT['email']}?subject={mail_subject}">{CONTACT['email']}</a>
        </div>
        <p class="small"><a href="tel:{CONTACT['tel']}">{CONTACT['tel_label']}</a> · <a href="{CONTACT['linkedin']}">LinkedIn</a> · <a href="{CONTACT['site']}">digitalessence.io</a></p>
      </div>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap">
    <p>Deze voorbeelden zijn gemaakt door Digital Essence, niet door of in opdracht van {esc(brand)}. Foto's, namen en productinformatie zijn van {esc(brand)} ({esc(data.get('domein', ''))}) en alleen gebruikt om te laten zien wat er kan. {ai_line}Liever dat deze pagina verdwijnt? Mail <a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a>, dan haal ik hem dezelfde dag offline.</p>
  </div>
</footer>

<dialog class="lb" aria-label="Advertenties groot">
  <div class="lb-track">{lb}</div>
  <div class="lb-bar">
    <button class="lb-prev" aria-label="Vorige">‹</button>
    <span class="lb-count"></span>
    <button class="lb-next" aria-label="Volgende">›</button>
  </div>
  <button class="lb-close" aria-label="Sluiten">✕</button>
</dialog>
<script src="../assets/site.js?v=3" defer></script>
</body>
</html>
"""
    (page / "index.html").write_text(out, "utf-8")
    print(f"✓ {slug}: {n} ads{', nieuwsbrief' if mail else ''} → {BASE_URL}/{slug}/")


if __name__ == "__main__":
    slugs = sys.argv[1:] or [p.stem for p in (ROOT / "brands").glob("*.json") if not p.stem.startswith("_")]
    for s in slugs:
        build(s)
