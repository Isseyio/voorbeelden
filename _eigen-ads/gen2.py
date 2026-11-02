"""Digital Essence — eigen Meta-lead-ads in DE-huisstijl (v2).
Concepten: EM (e-mailflows), MA (Meta-ads/creatives), AU (gratis audit).
python3 gen2.py [id ...]  -> html2/<id>.html ; render met render2.py
"""
import json, pathlib, base64, html as h, sys
ROOT = pathlib.Path(__file__).parent
N = json.loads((ROOT / 'niches2.json').read_text())

def img(k):
    f = ROOT / 'img' / f'{k}.jpg'
    return f"url(data:image/jpeg;base64,{base64.b64encode(f.read_bytes()).decode()}) center/cover no-repeat"

GRAD = {'EM': 'linear-gradient(160deg,#2C77B0 0%,#A387D6 100%)',
        'MA': 'linear-gradient(160deg,#EF6E73 0%,#FEB781 100%)',
        'WS': 'linear-gradient(160deg,#ED85D1 0%,#A1D3FF 100%)'}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;font-family:'DM Sans',Inter,sans-serif;-webkit-font-smoothing:antialiased}
.ad{position:relative;width:1080px;height:1920px;overflow:hidden;background:linear-gradient(180deg,#FFFFFF 0%,#EDEDFF 100%);color:#000}
.ad.dark{background:#000;color:#fff}
.inner{position:absolute;left:60px;right:60px;top:280px;display:flex;flex-direction:column;align-items:center}
.wm{font-size:30px;font-weight:400;letter-spacing:-.6px}
.pill{margin-top:26px;background:#ACACE6;color:#fff;font-size:25px;font-weight:500;padding:11px 26px;border-radius:999px;letter-spacing:-.2px}
h1{margin-top:26px;text-align:center;font-size:70px;line-height:1.06;font-weight:500;letter-spacing:-2.4px}
h1 i{font-style:italic;font-weight:500}
.sub{margin-top:22px;text-align:center;font-size:29px;line-height:1.4;color:#6E6E73;width:880px;letter-spacing:-.3px}
.dark .sub{color:#A1A1A6}
.card{margin-top:40px;width:960px;height:700px;border-radius:48px;position:relative;overflow:hidden}
.cta{margin-top:30px;background:#1E1515;color:#fff;font-family:Inter,sans-serif;font-weight:500;font-size:27px;padding:20px 40px;border-radius:999px}
.dark .cta{background:#fff;color:#1E1515}
/* phone */
.phone{position:absolute;width:320px;height:630px;border-radius:50px;background:#111;padding:11px;box-shadow:0 30px 60px rgba(0,0,0,.25)}
.scr{width:100%;height:100%;border-radius:40px;overflow:hidden;background:#fff;color:#111;position:relative;display:flex;flex-direction:column}
.notch{position:absolute;top:9px;left:50%;transform:translateX(-50%);width:86px;height:24px;border-radius:20px;background:#111;z-index:3}
/* flow */
.flow{position:absolute;left:44px;top:0;bottom:0;justify-content:center;width:500px;display:flex;flex-direction:column;gap:0}
.node{background:#fff;border-radius:24px;padding:24px 24px;display:flex;align-items:center;gap:16px;box-shadow:0 8px 24px rgba(20,20,60,.12)}
.node .ic{width:46px;height:46px;border-radius:14px;flex:none;display:flex;align-items:center;justify-content:center;font-size:24px}
.node b{display:block;font-size:24px;font-weight:600;letter-spacing:-.4px;color:#111}
.node span{display:block;font-size:18px;color:#6E6E73;margin-top:2px}
.link{width:3px;height:30px;background:rgba(255,255,255,.7);margin-left:44px}
.trig{color:#fff;font-size:20px;font-weight:500;opacity:.9;margin:0 0 14px 4px}
/* email */
.mhead{padding:40px 16px 10px;font-size:11px;color:#888;border-bottom:1px solid #eee}
.mhead b{display:block;color:#111;font-size:13px}
.mbrand{text-align:center;font-weight:700;letter-spacing:3px;font-size:15px;padding:12px 0}
.mimg{height:230px;flex:none}
.mbody{padding:14px 18px;text-align:center}
.mbody h3{font-size:20px;line-height:1.15;font-weight:700;letter-spacing:-.4px}
.mbody p{font-size:12.5px;color:#555;margin-top:8px;line-height:1.4}
.mbtn{margin:14px auto 0;color:#fff;font-size:13px;font-weight:700;padding:11px 18px;border-radius:999px;display:inline-block}
.code{margin-top:10px;font-size:12px;border:1.5px dashed #bbb;border-radius:8px;padding:6px 10px;display:inline-block;font-weight:700;letter-spacing:1px}
/* MA tiles */
.tile{position:absolute;width:250px;height:444px;border-radius:26px;overflow:hidden;box-shadow:0 24px 50px rgba(90,30,20,.28);border:6px solid #fff}
.tile .ov{position:absolute;left:0;right:0;padding:16px;color:#fff;font-weight:700;font-size:23px;line-height:1.1;letter-spacing:-.4px;text-shadow:0 2px 12px rgba(0,0,0,.35)}
.tile .top{top:0;background:linear-gradient(180deg,rgba(0,0,0,.45),transparent)}
.tile .bot{bottom:0;background:linear-gradient(0deg,rgba(0,0,0,.55),transparent);padding-top:40px}
.tile .rev{position:absolute;left:12px;right:12px;bottom:14px;background:#fff;color:#111;border-radius:14px;padding:10px 12px;font-size:14px;line-height:1.3;font-weight:500}
.tile .rev b{color:#F5B301;letter-spacing:1px}
.tile .ugc{position:absolute;left:12px;top:12px;background:rgba(0,0,0,.55);color:#fff;font-size:12px;padding:5px 9px;border-radius:999px}
.lbl{position:absolute;background:#fff;color:#111;font-size:21px;font-weight:600;padding:9px 18px;border-radius:999px;box-shadow:0 8px 20px rgba(0,0,0,.12)}
.week{position:absolute;left:40px;right:40px;bottom:34px;display:flex;gap:10px;justify-content:center}
.week span{background:rgba(255,255,255,.85);color:#C2504F;font-size:19px;font-weight:600;padding:8px 14px;border-radius:12px}
.week span.on{background:#1E1515;color:#fff}
/* AU */
.au{background:#fff;color:#111}
.store .hdr{height:44px;display:flex;align-items:center;justify-content:center;font-weight:700;letter-spacing:3px;font-size:14px;border-bottom:1px solid #eee;margin-top:36px}
.store .simg{height:260px;flex:none}
.store .sb{padding:12px 16px}
.store .sb b{font-size:17px;font-weight:600;display:block}
.store .sb span{font-size:14px;color:#555}
.store .sbtn{margin:12px 16px;height:40px;border:1.5px solid #bbb;border-radius:4px;font-size:13px;display:flex;align-items:center;justify-content:center;color:#333}
.mark{position:absolute;border:4px solid #EF6E73;border-radius:18px}
.note{position:absolute;width:390px;background:#fff;border-radius:22px;padding:16px 20px;box-shadow:0 12px 30px rgba(0,0,0,.18);display:flex;gap:14px;align-items:flex-start}
.note .n{flex:none;width:36px;height:36px;border-radius:50%;background:#EF6E73;color:#fff;font-weight:700;font-size:20px;display:flex;align-items:center;justify-content:center}
.note b{display:block;font-size:21px;font-weight:600;letter-spacing:-.3px;line-height:1.2;color:#111}
.note span{display:block;font-size:16.5px;color:#6E6E73;margin-top:4px;line-height:1.3}
.chips{position:absolute;left:470px;right:30px;bottom:44px;display:flex;gap:10px;justify-content:flex-start}
.chips span{color:#fff;font-size:20px;font-weight:600;padding:9px 18px;border-radius:999px}
"""

def head(n, ad):
    return f"""<div class="wm">Digital Essence</div><div class="pill">{h.escape(n['pill'])}</div>
<h1>{ad['headline']}</h1><div class="sub">{h.escape(ad['sub']).replace('e-mail','e‑mail').replace('Meta-ads','Meta‑ads')}</div>"""

def concept_em(n):
    m = n['mock']
    steps = [('👋', 'Welkomstmail', m['em_welkom']), ('🛒', 'Verlaten winkelwagen', 'na 1 uur, met je bestseller'),
             ('📦', 'Na aankoop', m['em_naaankoop']), ('💌', 'Winback', m['em_winback'])]
    flow = '<div class="trig">Trigger: aanmelding of bezoek</div>' + '<div class="link" style="height:34px"></div>'.join(
        f'<div class="node"><div class="ic" style="background:{c}">{ic}</div><div><b>{t}</b><span>{h.escape(s)}</span></div></div>'
        for (ic, t, s), c in zip(steps, ['#EEF3FA', '#FDEDEE', '#F1ECFA', '#FFF4EA']))
    phone = f"""<div class="phone" style="right:44px;top:36px"><div class="scr"><div class="notch"></div>
<div class="mhead"><b>{h.escape(m['brand'])}</b>{h.escape(m['em_subject'])}</div>
<div class="mbrand">{h.escape(m['brand'])}</div><div class="mimg" style="background:{img(m['img'])}"></div>
<div class="mbody"><h3>{h.escape(m['em_kop'])}</h3><p>{h.escape(m['em_tekst'])}</p>
<div class="code">WELKOM10</div><br><div class="mbtn" style="background:{m['color']}">Shop de collectie</div></div></div></div>"""
    return f'<div class="card" style="background:{GRAD["EM"]}"><div class="flow">{flow}</div>{phone}</div>'

def concept_ma(n):
    m = n['mock']; I = img(m['img'])
    t1 = f'<div class="tile" style="left:60px;top:120px;transform:rotate(-7deg);background:{I}"><div class="ov top">{h.escape(m["ma_hook"])}</div></div>'
    t2 = f'<div class="tile" style="left:355px;top:70px;z-index:2;background:{I}"><span class="ugc">UGC</span><div class="rev"><b>★★★★★</b><br>“{h.escape(m["ma_review"])}”</div></div>'
    t3 = f'<div class="tile" style="left:650px;top:120px;transform:rotate(7deg);background:{I}"><div class="ov bot">{h.escape(m["ma_static"])}</div></div>'
    labels = ('<span class="lbl" style="left:80px;top:40px">Hook-test</span>'
              '<span class="lbl" style="left:420px;top:16px;z-index:3">UGC</span>'
              '<span class="lbl" style="left:730px;top:40px">Static</span>')
    week = '<div class="week"><span>Ma · briefen</span><span>Wo · maken</span><span class="on">Vr · live</span><span>Ma · winnaars opschalen</span></div>'
    return f'<div class="card" style="background:{GRAD["MA"]}">{t1}{t2}{t3}{labels}{week}</div>'

def concept_au(n):
    m = n['mock']
    phone = f"""<div class="phone" style="left:60px;top:36px"><div class="scr store"><div class="notch"></div>
<div class="hdr">{h.escape(m['brand'])}</div><div class="simg" style="background:{img(m['img'])}"></div>
<div class="sb"><b>{h.escape(m['product'])}</b><span>€{m['price']},00 EUR</span></div><div class="sbtn">In winkelwagen</div>
<div class="sb" style="color:#aaa;font-size:12px;text-align:center;letter-spacing:2px">NIEUWSBRIEF</div></div></div>"""
    notes = [('Geen pop-up', 'Bezoekers vertrekken zonder dat je hun e-mailadres hebt.'),
             ('Geen flow na het winkelmandje', 'Wie afhaakt, hoort nooit meer iets van je.'),
             ('Ads sturen naar de homepage', 'In plaats van naar het product uit de advertentie.')]
    tops = [50, 225, 400]
    nh = ''.join(f'<div class="note" style="left:470px;top:{t}px"><div class="n">{i+1}</div><div><b>{h.escape(a)}</b><span>{h.escape(b)}</span></div></div>'
                 for i, ((a, b), t) in enumerate(zip(notes, tops)))
    chips = (f'<div class="chips"><span style="background:{GRAD["EM"]}">E-mailflows</span>'
             f'<span style="background:{GRAD["MA"]}">Meta-ads</span><span style="background:{GRAD["WS"]}">Webshop</span></div>')
    return f'<div class="card au" style="background:#F5F5F7">{phone}{nh}{chips}</div>'

def ad_defs(k, n):
    return [
        {'id': f'{k}-EM', 'concept': 'EM', 'dark': False,
         'headline': f"Laat je {n['label']} verkopen <i>terwijl je slaapt.</i>",
         'sub': 'Wij bouwen je Klaviyo-flows: welkom, verlaten winkelwagen, na aankoop en winback. Eén keer goed ingericht, elke dag omzet.'},
        {'id': f'{k}-MA', 'concept': 'MA', 'dark': False,
         'headline': f"Meta-ads die hun budget <i>terugverdienen.</i>",
         'sub': f"Elke week nieuwe creatives voor jouw {n['label']}. Wij bedenken, maken en testen. Wat werkt schalen we op."},
        {'id': f'{k}-AU', 'concept': 'AU', 'dark': True,
         'headline': f"Wij kijken gratis naar jouw {n['shop']}.",
         'sub': 'Waar je advertentiebudget weglekt, welke flows ontbreken en de drie dingen die wij als eerste zouden fixen. Geen deck, geen pitch.'},
    ]

def render(n, ad):
    body = {'EM': concept_em, 'MA': concept_ma, 'AU': concept_au}[ad['concept']](n)
    cta = 'Vraag je gratis audit aan'
    return (f'<div class="ad{" dark" if ad["dark"] else ""}" data-id="{ad["id"]}"><div class="inner">'
            f'{head(n, ad)}{body}<div class="cta">{cta} →</div></div></div>')

def doc(inner):
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{inner}</body></html>'

if __name__ == '__main__':
    out = ROOT / 'html2'; out.mkdir(exist_ok=True)
    want = set(sys.argv[1:])
    allads = []
    for k, n in N.items():
        for ad in ad_defs(k, n):
            if want and ad['id'] not in want and k not in want: continue
            html = render(n, ad); allads.append((ad, html))
            (out / f"{ad['id']}.html").write_text(doc(html))
    (ROOT / 'ads2.json').write_text(json.dumps([dict(a, niche=a['id'].rsplit('-',1)[0]) for a, _ in allads], ensure_ascii=False, indent=1))
    print(len(allads), 'ads')
