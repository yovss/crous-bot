from playwright.async_api import async_playwright
import time

BASE_URL = "https://trouverunlogement.lescrous.fr"
URL = f"{BASE_URL}/tools/47/search"


async def get_available_rooms():
    start = time.perf_counter()

    rooms = []
    seen = set()

    print("Opening browser...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        print("Loading page...")
        await page.goto(URL, wait_until="networkidle")

        print("Page loaded.")

        # Check if there are no accommodations
        if "Aucun logement trouvé" in await page.content():
            print("No rooms found.")
            await browser.close()
            return []

        # Find only accommodation links
        links = page.locator('a[href*="/accommodations/"]')
        count = await links.count()

        print(f"Found {count} accommodation links.\n")

        for i in range(count):

            link = links.nth(i)

            href = await link.get_attribute("href")

            if not href:
                continue

            if href in seen:
                continue

            seen.add(href)

            url = BASE_URL + href

            # Find the surrounding card
            card = link.locator("xpath=ancestor::article[1]")

            if await card.count() == 0:
                card = link.locator("xpath=ancestor::li[1]")

            text = (await card.inner_text()).strip()

            lines = [x.strip() for x in text.splitlines() if x.strip()]

            title = "Unknown"

            for line in lines:
                if "€" in line:
                    continue
                if len(line) > 3:
                    title = line
                    break

            room = {
                "title": title,
                "price": lines[0] if lines else "",
                "details": "\n".join(lines),
                "url": url,
            }

            rooms.append(room)

            # Live output
            print("=" * 60)
            print(f"ROOM #{len(rooms)}")
            print("Title :", room["title"])
            print("Price :", room["price"])
            print("Link  :", room["url"])

        await browser.close()

    elapsed = time.perf_counter() - start

    print("\nFinished!")
    print(f"Unique rooms found: {len(rooms)}")
    print(f"Time: {elapsed:.2f}s")

    return rooms


if __name__ == "__main__":
    import asyncio

    async def test():
        rooms = await get_available_rooms()

        print("\nSUMMARY")
        print("-" * 60)

        for room in rooms:
            print(room["title"])
            print(room["url"])
            print()

    asyncio.run(test())