#!/usr/bin/env python3
"""v7-voorbeeldpagina (17-11-2026): full-funnel, invalshoeken uitgelegd, 5 advertenties per fase.

Gebruik:  python3 tools/v7/build_page.py <slug>
Invoer:   brands/<slug>.json  (zie brands/_voorbeeld_v7.json)
          <slug>/src/ad1.png … ad5.png (1080x1920), mail.png, mail2.png (600 breed, 2x),
          optioneel product.png (uitgeknipt product, transparant)
Uitvoer:  <slug>/index.html, <slug>/img/*.jpg (+ product.png)
src/ wordt niet gecommit (.gitignore).
"""
import html, json, sys
from pathlib import Path
from urllib.parse import quote
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://voorbeelden.digitalessence.io"
WA = "31643003935"
MEET = "https://calendar.app.google/CyLvHxXww7ogm8699"
FASE = {
    "TOF": ("tof", "Stap 1 · Kennismaken", "Voor mensen die {merk} nog niet kennen."),
    "MOF": ("mof", "Stap 2 · Overtuigen", "Voor mensen die jullie kennen, maar nog twijfelen."),
    "BOF": ("bof", "Stap 3 · Kopen", "Voor wie bijna bestelt."),
}
e = lambda s: html.escape(str(s or ""), quote=True)


def imgs(slug, d):
    src, out = ROOT / slug / "src", ROOT / slug / "img"
    out.mkdir(parents=True, exist_ok=True)
    for i in range(1, len(d["advertenties"]) + 1):
        im = Image.open(src / f"ad{i}.png").convert("RGB")
        if im.size != (1080, 1920):
            im = im.resize((1080, 1920), Image.LANCZOS)
        im.save(out / f"ad{i}.jpg", quality=86, optimize=True, progressive=True)
        im.resize((540, 960), Image.LANCZOS).save(out / f"ad{i}-s.jpg", quality=84, optimize=True, progressive=True)
    for s, t in (("mail.png", "mail.jpg"), ("mail2.png", "mail2.jpg")):
        if (src / s).exists():
            im = Image.open(src / s).convert("RGB")
            if im.width > 1200:
                im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
            im.save(out / t, quality=84, optimize=True, progressive=True)
    if (src / "product.png").exists():
        im = Image.open(src / "product.png"); im.thumbnail((360, 520)); im.save(out / "product.png", optimize=True)


def build(slug):
    d = json.loads((ROOT / "brands" / f"{slug}.json").read_text())
    assert d.get("v") == 7, "geen v7-json"
    ads = d["advertenties"]
    order = {"TOF": 0, "MOF": 1, "BOF": 2}
    assert all(a["fase"] in order for a in ads), "fase moet TOF/MOF/BOF zijn"
    assert [order[a["fase"]] for a in ads] == sorted(order[a["fase"]] for a in ads), "advertenties op volgorde TOF → MOF → BOF"
    imgs(slug, d)
    merk, url = d["merk"], f"{BASE}/{slug}/"
    wa = f"https://wa.me/{WA}?text=" + quote(f"Hoi Issey, ik heb de voorbeelden voor {merk} gezien.")
    n = len(ads)
    intro = d.get("intro") or f"{n} advertenties en twee nieuwsbrieven, gemaakt met jullie eigen foto's en productinformatie."
    fan = d.get("fan") or [min(4, n), n, 1]
    fan_html = "".join(f'<img src="img/ad{i}-s.jpg" width="540" height="960" alt="" decoding="async">' for i in fan)
    p = d.get("product", {})
    p_img = (f'<img src="img/product.png" width="180" alt="{e(p.get("naam"))} van {e(merk)}" loading="lazy">'
             if (ROOT / slug / "src" / "product.png").exists() else "")
    angle_li = "".join(f'<li><em>{i:02d}</em><b>{e(a["invalshoek"][:1].upper() + a["invalshoek"][1:])}</b><span>"{e(a["vraag"])}"</span></li>'
                       for i, a in enumerate(ads, 1))
    groups, counts, idx = [], [], 0
    for f in ("TOF", "MOF", "BOF"):
        g = [a for a in ads if a["fase"] == f]
        if not g:
            continue
        cls, lab, sub = FASE[f]
        lis = ""
        for a in g:
            idx += 1
            lis += (f'<li class="ad"><button class="ad-btn" data-i="{idx-1}" aria-label="Bekijk advertentie {idx} groot">'
                    f'<img src="img/ad{idx}-s.jpg" srcset="img/ad{idx}-s.jpg 540w, img/ad{idx}.jpg 1080w" sizes="(min-width: 1100px) 250px, (min-width: 700px) 30vw, 70vw" '
                    f'width="540" height="960" alt="Advertentie {idx} voor {e(merk)}: {e(a.get("alt") or a["titel"])}" loading="{"eager" if idx < 3 else "lazy"}" decoding="async"></button>'
                    f'<div class="ad-meta"><span class="ad-n">{idx:02d}</span><h3>{e(a["titel"])}</h3><span class="ad-angle">Invalshoek: {e(a["invalshoek"])}</span><p>{e(a["waarom"])}</p></div></li>')
        groups.append(f'<div class="stage-group" style="--n:{len(g)}"><div class="stage-head"><span class="stage {cls}"><i></i>{lab}</span><p>{e(sub.format(merk=merk))}</p></div><ul class="ads" role="list">{lis}</ul></div>')
        counts.append(f"{len(g)}fr")
    slides = "".join(f'<figure class="lb-slide"><img src="img/ad{i}.jpg" width="1080" height="1920" alt="Advertentie {i}: {e(a["titel"])}" loading="lazy" decoding="async">'
                     f'<figcaption>{i:02d} · {FASE[a["fase"]][1].split(" · ")[1]} · {e(a["invalshoek"][:1].upper() + a["invalshoek"][1:])}</figcaption></figure>'
                     for i, a in enumerate(ads, 1))
    w = d["waarom"]
    stats = "".join(f'<div><strong>{e(s["getal"])}</strong><span>{e(s["label"])}</span></div>' for s in w["stats"])
    bron = f'<p class="small">{e(w["bron"])}</p>' if w.get("bron") else ""
    mails = ""
    for k, m in enumerate(d["nieuwsbrieven"][:2]):
        f = "mail.jpg" if k == 0 else "mail2.jpg"
        ticks = "".join(f"<li>{e(t)}</li>" for t in m.get("punten", []))
        mails += (f'<section class="sec mail-sec{" mail-sec-2" if k else ""}" id="nieuwsbrief{"-2" if k else ""}"><div class="wrap mail-grid"><div class="mail-copy">'
                  f'<p class="eyebrow">Nieuwsbrief {k+1} van 2 · {e(m["type"])}</p><h2>{e(m["kop"])}</h2><p class="lead">{e(m["tekst"])}</p><ul class="ticks">{ticks}</ul></div>'
                  f'<div class="mail-frame"><div class="mail-head"><div class="mail-av" style="background:{e(d["accent"])}">{e(merk[:1].upper())}</div>'
                  f'<div class="mail-from"><strong>{e(merk)}</strong><span>{e(m["onderwerp"])}</span></div></div>'
                  f'<div class="mail-body"><img src="img/{f}" width="1200" alt="Voorbeeldnieuwsbrief voor {e(merk)}" loading="lazy" decoding="async"></div>'
                  f'<button class="mail-more" type="button">Lees de hele nieuwsbrief</button></div></div></section>')
    obs = f'<p class="obs">{e(d["funnel_obs"])}</p>' if d.get("funnel_obs") else ""
    ai = (" Sommige sfeerbeelden zijn deels met AI gemaakt; de producten zijn jullie eigen productfoto's." if d.get("ai_sfeer") else "")
    pz = d.get("product_zin", "Hetzelfde product")
    page = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Voorbeelden voor {e(merk)} · Digital Essence</title>
<meta name="description" content="{e(intro)}">
<meta property="og:type" content="website">
<meta property="og:title" content="Voorbeelden voor {e(merk)}">
<meta property="og:description" content="{e(intro)}">
<meta property="og:image" content="{url}img/ad1-s.jpg">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FBEFC8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css?v=7">
<link rel="stylesheet" href="../assets/v7.css?v=2">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<style>:root{{--brand:{e(d["accent"])}}}</style>
</head>
<body>
<header class="top"><div class="wrap top-in"><a class="logo" href="https://digitalessence.io" aria-label="Digital Essence">Digital Essence</a><a class="pill pill-wa" href="{wa}">WhatsApp</a></div></header>
<main>
<section class="hero"><div class="wrap hero-grid"><div class="hero-copy">
<p class="eyebrow"><span class="dot"></span>Voorbeelden voor {e(merk)}</p>
<h1>{e(d["kop"])}</h1>
<p class="lead">{e(intro)} Een idee van Issey Kooijmans van Digital Essence; niets hiervan is gepubliceerd.</p>
<div class="hero-cta"><a class="btn btn-dark" href="#advertenties">Bekijk de voorbeelden</a><a class="btn btn-ghost" href="#contact">Even sparren?</a></div>
</div><div class="fan" aria-hidden="true">{fan_html}</div></div></section>

<section class="sec note-sec"><div class="wrap"><div class="note"><div class="me"><div class="me-photo me-mono" aria-hidden="true">IK</div><div><strong>Issey Kooijmans</strong><span>Digital Essence · Utrecht</span></div></div>
<p>{e(d["noot"])}</p></div></div></section>

<section class="sec" id="invalshoek"><div class="wrap">
<p class="eyebrow">Eerst even uitgelegd</p><h2>Wat is een invalshoek?</h2>
<p class="lead">Een invalshoek is de reden waarom iemand iets koopt. {e(pz)} kun je op heel veel manieren verkopen, omdat niet iedereen om dezelfde reden koopt.</p>
<div class="angle-box"><div class="angle-prod"><span class="stage tof"><i></i>Eén product</span>
<div class="angle-row"><div><div class="big" style="margin-top:14px">{e(p.get("naam", merk))}</div><p>{e(p.get("tekst") or f"Hetzelfde product, {n} verschillende redenen om het te kopen. Elke reden wordt een eigen advertentie.")}</p></div>{p_img}</div></div>
<ol class="angle-list">{angle_li}</ol></div>
<p class="angle-end">We testen die invalshoeken naast elkaar. Na een paar dagen zie je welke het meest verkoopt. Daar maken we er meer van, en wat niet werkt, gaat eruit.</p>
</div></section>

<section class="sec" id="funnel"><div class="wrap">
<p class="eyebrow">Zo werk ik</p><h2>Van eerste blik tot bestelling.</h2>
<p class="lead">Niet iedereen die een advertentie ziet, is meteen klaar om te kopen. Daarom maak ik voor elke stap andere advertenties. Zo spreek je iedereen aan op het moment waar hij of zij zit.</p>
<ol class="funnel">
<li><div class="bar"><i></i></div><span class="n">Stap 1 · Top of funnel</span><h3>Kennismaken</h3><p class="who">Mensen die {e(merk)} nog nooit hebben gezien.</p><p class="goal">Doel: dat ze stoppen met scrollen en nieuwsgierig worden.</p><p class="like">Zoals een etalage: je loopt langs en kijkt even naar binnen.</p></li>
<li><div class="bar"><i></i></div><span class="n">Stap 2 · Middle of funnel</span><h3>Overtuigen</h3><p class="who">Mensen die jullie al eens zagen, maar nog twijfelen.</p><p class="goal">Doel: hun vragen beantwoorden. Wat is het, waarom dit en niet iets anders?</p><p class="like">Zoals een verkoper die rustig uitlegt wat het verschil is.</p></li>
<li><div class="bar"><i></i></div><span class="n">Stap 3 · Bottom of funnel</span><h3>Kopen</h3><p class="who">Mensen die bijna willen bestellen.</p><p class="goal">Doel: het laatste duwtje, zoals een aanbod, reviews of de zekerheid van gratis retour.</p><p class="like">Zoals de kassa: duidelijk, makkelijk en zonder risico.</p></li>
</ol>{obs}
</div></section>

<section class="sec" id="advertenties"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">Advertenties · 9:16</p><h2>{"Vijf" if n == 5 else n} advertenties, verdeeld over de stappen.</h2></div><p class="hint">Tik op een advertentie om hem groot te bekijken.</p></div>
<div class="stages" style="--cols:{' '.join(counts)}">{"".join(groups)}</div>
</div></section>

<section class="sec why-sec" id="waarom"><div class="wrap">
<p class="eyebrow">Waarom advertenties</p><h2>{e(w["kop"])}</h2><p class="lead">{e(w["tekst"])}</p>
<div class="stats">{stats}</div>{bron}
</div></section>
{mails}
<section class="sec week-sec"><div class="wrap">
<p class="eyebrow">Ritme</p><h2>Zo kan een week eruitzien.</h2>
<p class="lead">Dit is een voorbeeld, geen vast pakket. De kracht zit in het ritme: regelmatig nieuwe invalshoeken testen in elke stap, en je nieuwsbrief vast versturen. Wat werkt, doen we vaker.</p>
<ol class="week"><li><span class="day">Ma</span><strong>Nieuwe advertenties live</strong><span class="sub">Nieuwe invalshoeken in elke stap tegelijk testen.</span></li><li><span class="day">Di</span><strong>Meekijken</strong><span class="sub">Welke invalshoek pakt de doelgroep op?</span></li><li><span class="day">Wo</span><strong>Bijsturen</strong><span class="sub">Budget naar wat werkt, de rest eruit.</span></li><li><span class="day">Do</span><strong>Nieuwsbrief verstuurd</strong><span class="sub">Vast moment, zodat lezers erop gaan rekenen.</span></li><li><span class="day">Vr</span><strong>Korte update</strong><span class="sub">Wat werkte en wat we volgende week doen.</span></li></ol>
<div class="facts"><div><strong>Advertenties</strong><span>zoveel als bij jullie past, in elke stap</span></div><div><strong>Nieuwsbrief</strong><span>per week, of vaker als dat beter werkt</span></div><div><strong>Vrij</strong><span>per week, per maand of per campagne</span></div></div>
</div></section>

<section class="sec contact-sec" id="contact"><div class="wrap"><div class="contact-card">
<div class="me"><div class="me-photo me-mono" aria-hidden="true">IK</div><div><strong>Issey Kooijmans</strong><span>Founder Digital Essence · Utrecht</span></div></div>
<h2>Benieuwd hoe dit voor {e(merk)} werkt?</h2><p class="lead">Een kwartiertje bellen is genoeg om te kijken of het past. Geen verplichtingen.</p>
<div class="cta-stack"><a class="btn btn-wa" href="{wa}">Stuur me een WhatsApp</a><a class="btn btn-meet" href="{MEET}">Plan een videogesprek</a><a class="btn btn-ghost" href="mailto:issey@digitalessence.io?subject={quote('Voorbeelden voor ' + merk)}">issey@digitalessence.io</a></div>
<p class="small"><a href="tel:+31643003935">+31 6 43003935</a> · <a href="https://www.linkedin.com/in/isseyk">LinkedIn</a> · <a href="https://digitalessence.io">digitalessence.io</a></p>
</div></div></section>
</main>
<footer class="foot"><div class="wrap"><p>Deze voorbeelden zijn gemaakt door Digital Essence, niet door of in opdracht van {e(merk)}. Foto's, namen, reviews en productinformatie zijn van {e(merk)} ({e(d["domein"])}) en alleen gebruikt om te laten zien wat er kan.{ai} Liever dat deze pagina verdwijnt? Mail <a href="mailto:issey@digitalessence.io">issey@digitalessence.io</a>, dan haal ik hem dezelfde dag offline.</p></div></footer>
<dialog class="lb" aria-label="Advertenties groot"><div class="lb-track">{slides}</div>
<div class="lb-bar"><button class="lb-prev" aria-label="Vorige">‹</button><span class="lb-count"></span><button class="lb-next" aria-label="Volgende">›</button></div>
<button class="lb-close" aria-label="Sluiten">✕</button></dialog>
<script src="../assets/site.js?v=7" defer></script>
</body>
</html>
'''
    (ROOT / slug / "index.html").write_text(page)
    print("ok", url)


if __name__ == "__main__":
    build(sys.argv[1])
