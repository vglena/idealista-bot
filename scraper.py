from playwright.sync_api import sync_playwright
import json
import re

URL = "https://www.idealista.com/venta-viviendas/madrid-provincia/con-publicado_ultimas-48-horas/?ordenado-por=fecha-publicacion-desc"

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, timeout=60000)
    page.wait_for_load_state("networkidle")

    # Esperar a que aparezcan listados
    page.wait_for_selector("article", timeout=10000)

    articles = page.query_selector_all("article")

    for article in articles:
        link_element = article.query_selector("a")
        if link_element:
            href = link_element.get_attribute("href")
            if href and "/inmueble/" in href:
                full_link = "https://www.idealista.com" + href
                match = re.search(r'/inmueble/(\d+)/', full_link)
                if match:
                    results.append({
                        "id": match.group(1),
                        "url": full_link
                    })

    browser.close()

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

