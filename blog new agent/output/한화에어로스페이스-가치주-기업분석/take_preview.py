import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def capture_preview():
    html_file = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\한화에어로스페이스-가치주-기업분석\final.html")
    output_png = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\한화에어로스페이스-가치주-기업분석\preview_page.png")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1.5)
        await page.goto(html_file.as_uri(), wait_until="networkidle")
        await page.screenshot(path=str(output_png), full_page=True)
        await browser.close()
        print(f"[미리보기 캡처 완료] {output_png}")

if __name__ == "__main__":
    asyncio.run(capture_preview())
