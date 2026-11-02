import sys, pathlib, asyncio
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).parent

async def main(ids):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for i in ids:
            await pg.goto((ROOT / 'html2' / f'{i}.html').as_uri())
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=str(ROOT / 'png2' / f'{i}.png'))
            print('png', i)
        await b.close()

ids = sys.argv[1:] or [f.stem for f in (ROOT / 'html2').glob('*.html')]
asyncio.run(main(ids))
