from playwright.sync_api import sync_playwright
import json
import re

URL = "https://www.idealista.com/venta-viviendas/madrid-provincia/con-publicado_ultimas-48-horas/?ordenado-por=fecha-publicacion-desc"

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)
    page.wait_for_timeout(5000)

    links = page.query_selector_all('a.item-link')

    for link in links[:20]:
        href = link.get_attribute("href")
        if href:
            full_link = "https://www.idealista.com" + href
            match = re.search(r'/inmueble/(\d+)/', full_link)
            if match:
                results.append({
                    "id": match.group(1),
                    "url": full_link
                })

    browser.close()

with open("results.json", "w") as f:
    json.dump(results, f)
