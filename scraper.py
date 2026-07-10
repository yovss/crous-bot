import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://trouverunlogement.lescrous.fr"
URL = f"{BASE_URL}/tools/47/search"


async def get_available_rooms():
    rooms = []
    seen = set()

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(URL)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.select('a[href*="/accommodations/"]'):
        href = link.get("href")
        if not href or href in seen:
            continue

        seen.add(href)

        rooms.append({
            "title": link.get_text(strip=True),
            "price": "",
            "url": BASE_URL + href,
        })

    return rooms