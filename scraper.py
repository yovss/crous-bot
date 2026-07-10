import httpx
import asyncio
from bs4 import BeautifulSoup

BASE_URL = "https://trouverunlogement.lescrous.fr"
SEARCH_URL = f"{BASE_URL}/tools/47/search"


async def get_available_rooms():
    rooms = []
    seen = set()
    page = 1  # Start at page 1

    # Added a timeout to prevent hanging connections
    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
        while True:
            # Add the ?page=X query to the URL
            url = f"{SEARCH_URL}?page={page}"
            
            try:
                response = await client.get(url)
                response.raise_for_status()
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break  # Stop if the website is down or gives a 404

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.select('a[href*="/accommodations/"]')

            # If no accommodation links are found on this page, we reached the end!
            if not links:
                break

            new_rooms_on_page = False

            for link in links:
                href = link.get("href")
                if not href or href in seen:
                    continue

                # We found a completely new room
                new_rooms_on_page = True
                seen.add(href)

                rooms.append({
                    "title": link.get_text(strip=True),
                    "price": "", 
                    "url": BASE_URL + href,
                })

            # If the page only contained links we've already seen (sometimes 
            # websites default to page 1 if you go out of bounds), stop looping.
            if not new_rooms_on_page:
                break

            # Move to the next page
            page += 1
            
            # Wait 1 second before fetching the next page so CROUS doesn't block your bot
            await asyncio.sleep(1)

    return rooms