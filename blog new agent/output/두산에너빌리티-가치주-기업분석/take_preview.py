import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def capture_preview():
    html_path = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\두산에너빌리티-가치주-기업분석\final.html").resolve()
    out_path = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\두산에너빌리티-가치주-기업분석\preview_page.png")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1200, "height": 1800}, device_scale_factor=1.5)
        await page.goto(f"file:///{html_path}", wait_until="networkidle")
        await page.screenshot(path=str(out_path), full_page=True)
        await browser.close()
        print("Captured full page preview!")

if __name__ == "__main__":
    asyncio.run(capture_preview())
