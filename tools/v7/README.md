# v7-voorbeeldpagina's (vanaf 17-11-2026)

Vijf advertenties verdeeld over de funnel (standaard 2 TOF, 2 MOF, 1 BOF), elk met een eigen invalshoek, plus twee nieuwsbrieven.
De pagina legt in gewone taal uit wat een invalshoek is en hoe de funnel werkt. De volledige werkwijze staat in het (privé) project "Cold outreach workflow": templates/outreach-v7.md.

1. Werkmap buiten de repo, bv. /home/claude/work/<slug>/: per advertentie een HTML-bestand (ad1.html … ad5.html, 1080x1920) en mail.html, mail2.html (600 breed), met de echte lettertypen van het merk (@fontsource via `npm pack`) en de echte foto's van het merk.
2. `python3 tools/v7/cutout.py` voor uitgeknipte producten (origineel product, alleen achtergrond weg).
3. `python3 tools/v7/render.py <werkmap> <slug>` → `<slug>/src/*.png` en `<werkmap>/_controle.jpg` (bekijken en verbeteren).
4. `brands/<slug>.json` met `"v":7` (zie brands/sanvri-kfzfp.json); advertenties op volgorde TOF → MOF → BOF; optioneel `<slug>/src/product.png`.
5. `python3 tools/v7/build_page.py <slug>` → `<slug>/index.html` en `<slug>/img/`.
6. Committen en pushen naar main (eerst `git fetch --depth=1 origin main && git rebase origin/main`). Nooit `src/` committen.

v7-pagina's laden `assets/site.css` + `assets/v7.css`. Oudere pagina's blijven ongewijzigd.
