#!/usr/bin/env python3
"""Rendert advertenties en nieuwsbrieven uit HTML naar PNG (Chrome headless via Playwright).

Gebruik: python3 tools/v7/render.py <werkmap> <slug-map>
  <werkmap>/ad1.html … ad5.html  -> <slug-map>/src/ad1.png … (1080x1920)
  <werkmap>/mail.html, mail2.html -> <slug-map>/src/mail.png, mail2.png (600 breed, 2x, hele hoogte)
Daarna maakt het <werkmap>/_controle.jpg: alle advertenties naast elkaar, om te bekijken.
"""
import asyncio, sys
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

async def main(work: Path, dest: Path):
    out = dest / "src"; out.mkdir(parents=True, exist_ok=True)
    exe = next((p for p in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser") if Path(p).exists()), None)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=exe, args=["--allow-file-access-from-files"]) if exe else await p.chromium.launch()
        ad = await b.new_page(viewport={"width": 1080, "height": 1920})
        ml = await b.new_page(viewport={"width": 600, "height": 900}, device_scale_factor=2)
        for f in sorted(work.glob("ad*.html")):
            await ad.goto(f.resolve().as_uri()); await ad.evaluate("document.fonts.ready"); await ad.wait_for_timeout(400)
            await ad.screenshot(path=str(out / (f.stem + ".png")))
        for f in sorted(work.glob("mail*.html")):
            await ml.goto(f.resolve().as_uri()); await ml.evaluate("document.fonts.ready"); await ml.wait_for_timeout(500)
            await ml.screenshot(path=str(out / (f.stem + ".png")), full_page=True)
        await b.close()
    ads = sorted(out.glob("ad*.png"))
    if ads:
        sheet = Image.new("RGB", (len(ads) * 550, 960), "white")
        for k, f in enumerate(ads):
            sheet.paste(Image.open(f).convert("RGB").resize((540, 960)), (k * 550, 0))
        sheet.save(work / "_controle.jpg", quality=82)
    print("ok", [f.name for f in sorted(out.glob("*.png"))])

if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1]), Path(sys.argv[2])))
