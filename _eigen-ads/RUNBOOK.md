# Eigen Meta-ads Digital Essence: runbook voor de wekelijkse run

Doel: elke week automatisch nieuwe niche-advertenties voor Digital Essence zelf maken (Figma, bewerkbaar), hosten,
in Meta zetten in de bestaande leadformuliercampagne en verliezers pauzeren. Focus: **Meta-ads en e-mailmarketing**;
CRO alleen als onderdeel van de gratis audit.

## Huisstijl (van digitalessence.io, niet afwijken)
- Lettertype DM Sans (koppen 500, strak letterspacing); knoppen Inter 500.
- Licht verloop #FFFFFF → #EDEDFF; donkere variant #000.
- Pillabel lavendel #ACACE6 met witte tekst; knoppen zwart #1E1515 (op zwart: wit).
- Dienstverlopen: e-mail #2C77B0→#A387D6, Meta-ads #EF6E73→#FEB781, webshop #ED85D1→#A1D3FF. Radius 24 (48 op 1080px).
- Woordmerk "Digital Essence" bovenaan. CTA in beeld: "Vraag je gratis audit aan →".
- Nooit de referentie-ads van derden namaken. Geen verzonnen resultaten, percentages of garanties voor Digital Essence.
  Mockup-merken in de beelden zijn fictief (LUMÉ, NORTHSIDE, …); voorbeeldreviews alleen binnen zo'n fictieve mock.

## Concepten (gen2.py)
- **EM**: "Laat je {niche}merk verkopen terwijl je slaapt." Flowdiagram + welkomstmail in de niche.
- **MA**: "Meta-ads die hun budget terugverdienen." Waaier hook-test / UGC / static + weekritme.
- **AU**: "Wij kijken gratis naar jouw {niche}webshop." Webshop met 3 aantekeningen (pop-up, flow, ads→homepage).
- Nieuw concept toevoegen mag (bv. **HK**: hook uit subniches.json als kop), maar altijd in deze huisstijl.

## Advertentieteksten (primaire tekst / kop / CTA APPLY_NOW)
- EM: "Draait je {label} wel ads, maar gebeurt er na de eerste bestelling niks meer?\n\nWij bouwen je e-mailflows in Klaviyo: een welkomstmail die verkoopt, een herinnering bij een verlaten winkelwagen, opvolging na aankoop en een winback voor klanten die wegblijven. Eén keer goed ingericht, elke dag omzet.\n\nVraag een gratis audit aan. Je krijgt de drie dingen die wij als eerste zouden fixen. Geen deck, geen pitch." / Kop: "Gratis audit van je e-mailflows"
- MA: "Elke week nieuwe ads voor je {label}, zonder dat jij er zelf mee bezig bent.\n\nWij bedenken de invalshoeken, maken de creatives (static, UGC en video) en testen ze in een vast ritme. Wat werkt schalen we op, wat niet werkt gaat eruit.\n\nBenieuwd waar je advertentiebudget nu weglekt? Vraag een gratis audit aan. Geen deck, geen pitch." / Kop: "Gratis audit van je Meta-ads"
- AU: "Wij kijken gratis naar je {shop}.\n\nWaar lekt je advertentiebudget weg? Welke e-mailflows ontbreken of presteren onder de maat? En wat zouden wij als eerste fixen?\n\nJe krijgt drie concrete punten terug. Geen deck, geen pitch. Gewoon wat wij zouden doen." / Kop: "Gratis audit van je webshop"
- Gebruik **geen** cijfers uit `hook_idee` in advertenties tenzij ze aantoonbaar kloppen (ze komen uit onderzoek en zijn niet geverifieerd).

## Wekelijkse run, stap voor stap
1. `git clone --depth 1 https://github.com/Isseyio/voorbeelden` (push-rechten nodig; via add_repo). Lees `state.json`.
2. Fonts: `mkdir -p ~/.fonts && curl -sSL -o ~/.fonts/DMSans.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf" && fc-cache -f`.
3. Kies de **2 volgende subniches** met status `open` in `subniches.json` (afwisselend per cluster). Zet ze in `niches2.json`
   met een fictief mockmerk, productnaam, prijs, merkkleur en de EM/MA-teksten (zie bestaande items als voorbeeld).
4. Productfoto per subniche: Figma `generate_image` in bestand `figma_file_key` (pagina "Assets · productfoto’s"),
   download de URL, sla op als `img/<key>.jpg` (max 900px, jpg q86). Kost Figma AI-credits: max 2 per run.
5. `python3 gen2.py <key1> <key2>` en `python3 render2.py` → controleer elke PNG visueel (geen afgekapte tekst,
   koppen max 3 regels, inhoud tussen y=280 en y=1630 zodat de 4:5-uitsnede klopt).
6. Figma: `html_to_figma` (cssSelector `.ad`) → nieuwe pagina "Ronde N · datum"; frames hernoemen `DE-RN-<key>-<concept>`.
7. Hosten: jpg's (q93) naar `../ma-k7w3q/rN/DE-RN-<key>-<concept>.jpg`, commit + push naar main, ~2 min wachten.
8. Meta: `ads_creative_upload_media` (URL) per beeld → hash. Als `adset_id` en `lead_gen_form_id` gevuld zijn: per beeld
   `ads_create_ad` in die adset met object_story_spec link_data {image_hash, message, name (kop), link "https://digitalessence.io",
   call_to_action {type: APPLY_NOW, value: {lead_gen_form_id}}}. Advertentienaam `DE-RN-<key>-<concept>`.
   Activeer de nieuwe ads alleen als de campagne zelf al actief is. **Nooit** budget, targeting of formulier aanpassen.
9. Optimaliseren (alleen als de campagne actief is): pauzeer ads die ≥ €30 hebben uitgegeven met 0 leads en minstens 7 dagen draaien;
   houd max ~10 actieve ads (pauzeer de duurste kosten per lead). Nooit de enige actieve ad pauzeren.
10. Werk `state.json` (ads, ronde) en `subniches.json` (status → `ronde N`) bij, commit + push.
11. Stuur Issey een korte samenvatting: nieuwe ads (met Figma-link), gepauzeerde ads, leads en kosten per lead per concept/niche
    van de afgelopen 7 dagen. Ontbreekt adset/formulier nog: zeg dat en noem wat hij moet doen.
