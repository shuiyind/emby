import asyncio
import os
import io
import argparse
from playwright.async_api import async_playwright
from PIL import Image

# Adblock list (simplified, from a public source)
# In a real-world scenario, you would use a more comprehensive and updated list.
BLOCK_LIST = [
    "adservice.google.com",
    "googlesyndication.com",
    "doubleclick.net",
    "google-analytics.com",
    "ads.pubmatic.com",
    "ad.turn.com",
    "criteo.com",
]

async def block_ads(route):
    """Block requests to domains in the block list."""
    if any(domain in route.request.url for domain in BLOCK_LIST):
        print(f"Blocking request to: {route.request.url}")
        await route.abort()
    else:
        await route.continue_()

async def take_screenshot(url: str, output_path: str = "screenshot.png"):
    """
    Takes a screenshot of a given URL with specific requirements.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 1024},
            java_script_enabled=True,
            accept_downloads=False,
        )
        page = await context.new_page()

        # Block ads and pop-ups by intercepting network requests
        await page.route("**/*", block_ads)

        # Handle dialogs (pop-ups) by automatically dismissing them
        page.on("dialog", lambda dialog: dialog.dismiss())

        try:
            print(f"Navigating to {url}...")
            # Increased timeout to handle potential delays from services like Cloudflare
            await page.goto(url, wait_until="networkidle", timeout=90000)

            print("Taking screenshot...")
            screenshot_bytes = await page.screenshot(path=None, full_page=False)

            # Compress image to meet size requirements
            print("Compressing image...")
            img = Image.open(io.BytesIO(screenshot_bytes))
            
            # Save with optimization
            quality = 85 
            img.save(output_path, "PNG", optimize=True, quality=quality)

            # Reduce quality until file size is under 2MB
            while os.path.getsize(output_path) > 2 * 1024 * 1024 and quality > 10:
                quality -= 5
                print(f"File size is too large. Retrying with quality={quality}...")
                img.save(output_path, "PNG", optimize=True, quality=quality)

            if os.path.getsize(output_path) > 2 * 1024 * 1024:
                print("Could not compress the image to under 2MB.")
            else:
                print(f"Screenshot saved to {output_path}")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take a screenshot of a webpage.")
    parser.add_argument("url", help="The URL of the webpage to screenshot.")
    parser.add_argument("-o", "--output", default="screenshot.png", help="Output file name for the screenshot.")
    args = parser.parse_args()

    url = args.url
    if not url.startswith("http://") and not url.startswith("https://"):
        print(f"URL '{url}' is missing a scheme. Prepending 'https://'.")
        url = "https://" + url

    asyncio.run(take_screenshot(url, args.output))