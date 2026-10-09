import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def take_preview():
    html_file = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\삼성중공업-가치주-기업분석\final.html")
    preview_img = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\삼성중공업-가치주-기업분석\preview_page.png")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1200, "height": 800}, device_scale_factor=1.5)
        await page.goto(f"file:///{html_file.as_posix()}", wait_until="networkidle")
        await page.screenshot(path=str(preview_img), full_page=True)
        await browser.close()
        print("Full page preview generated!")

if __name__ == "__main__":
    asyncio.run(take_preview())
