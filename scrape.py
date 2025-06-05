import json
from playwright.sync_api import sync_playwright

def scrape_levi_product_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")

        products = page.query_selector_all("div.product-tile")  # main container

        result = []

        for product in products:
            try:
                name = product.query_selector("a.name-link").inner_text().strip()
                price = product.query_selector(".product-sales-price").inner_text().strip()
                img = product.query_selector("img").get_attribute("src")
                detail_link = product.query_selector("a.name-link").get_attribute("href")

                # Go deeper into product page for more detail (optional)
                full_detail = ""
                if detail_link:
                    detail_url = "https://www.levi.com" + detail_link
                    detail_page = browser.new_page()
                    detail_page.goto(detail_url, timeout=60000)
                    detail_page.wait_for_load_state("networkidle")
                    detail_elem = detail_page.query_selector(".product-description")  # may vary
                    full_detail = detail_elem.inner_text().strip() if detail_elem else ""
                    detail_page.close()

                result.append({
                    "category": "Men/Women/Kids/Whatever",  # You can extract this from URL or breadcrumb if needed
                    "product_name": name,
                    "product_price": price,
                    "product_detail": full_detail,
                    "product_image": img
                })
            except Exception as e:
                print(f"Skipping a product due to error: {e}")
                continue

        browser.close()
        return result

# 👇 Example usage
if __name__ == "__main__":
    input_url = "https://www.levi.com/US/en_US/"
    data = scrape_levi_product_page(input_url)

    # Save to JSON
    with open("levi_products.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Scraping complete. Output saved to 'levi_products.json'")
