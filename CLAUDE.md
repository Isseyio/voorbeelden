# voorbeelden.digitalessence.io

Per merk één statische voorbeeldpagina voor de cold outreach van Digital Essence (Issey Kooijmans).
Gehost via GitHub Pages op voorbeelden.digitalessence.io (CNAME bij Hostnet → isseyio.github.io).

## Nieuwe pagina toevoegen (productierun)
1. Slug = `<merk-kort>-<5 willekeurige tekens>` (a-z, 2-9, geen 0/1/i/l/o), bv. `sevensocks-msrs6`. Niet te raden; nooit een lijst van merken publiceren.
2. Exporteer uit Figma (download_assets, png, scale 2) de ads en de nieuwsbrief naar `<slug>/src/ad1.png … adN.png` en `<slug>/src/mail.png`. `src/` wordt niet gecommit.
3. Schrijf `brands/<slug>.json` (zie `brands/_voorbeeld.json`): accent = primaire merkkleur, per ad een titel + één zin waarom.
4. `python3 tools/build.py <slug>` → `<slug>/index.html`, `<slug>/img/*.webp`, `og.jpg`.
5. Commit + push naar `main`. Link: `https://voorbeelden.digitalessence.io/<slug>/` → in de Sheet (kolom Deelbestand) en achter de zwarte knop "Bekijk de voorbeelden" in de mail.

## Regels
- Pagina's zijn noindex en robots.txt blokkeert alles; de root toont geen merken.
- Nooit suggereren dat het merk klant is of opdracht gaf (footer-disclaimer blijft staan).
- Productfoto's echt en onveranderd; de week-sectie noemt geen vast aantal ads.
- Merk vraagt om verwijdering → map `<slug>/` en `brands/<slug>.json` verwijderen en pushen, dezelfde dag.
- Foto van Issey: zet `assets/issey.jpg` (vierkant, ≥192px) en bouw opnieuw; anders monogram.
