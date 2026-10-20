import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    base_dir = Path(r"c:\Users\immnu\Desktop\Claud\blog new agent\output\20261020-오늘의-증시-시황-마켓브리핑")
    html_file = base_dir / "final.html"
    out_file = base_dir / "preview_page.png"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1.5)
        await page.goto(html_file.as_uri(), wait_until="networkidle")
        # Scroll down to ensure all images render
        await page.evaluate("""async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 400;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if(totalHeight >= scrollHeight){
                        clearInterval(timer);
                        window.scrollTo(0, 0);
                        resolve();
                    }
                }, 50);
            });
        }""")
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(out_file), full_page=True)
        await browser.close()
    print("Preview captured successfully:", out_file)

if __name__ == "__main__":
    asyncio.run(main())
