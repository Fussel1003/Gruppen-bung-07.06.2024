from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Initialisiere den Webdriver
driver = webdriver.Firefox()

# Öffne die Webseite
driver.get("http://books.toscrape.com")

# Funktion, um Buchinformationen zu sammeln
def scrape_books_from_category(category_url):
    driver.get(category_url)
    books_data = []

    while True:
        books = driver.find_elements(By.CLASS_NAME, "product_pod")

        for book in books:
            title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
            price = book.find_element(By.CLASS_NAME, "price_color").text
            availability = book.find_element(By.CLASS_NAME, "availability").text.strip()
            books_data.append({"title": title, "price": price, "availability": availability})

        try:
            next_button = driver.find_element(By.CLASS_NAME, "next")
            next_button.find_element(By.TAG_NAME, "a").click()
            time.sleep(2)
        except:
            break

    return books_data

# Kategorien auswählen
categories = {
    "travel": "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    "mystery": "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    "historical_fiction": "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
}

# Bücher aus den Kategorien sammeln und speichern
for category, url in categories.items():
    books = scrape_books_from_category(url)
    with open(f"{category}.json", "w", encoding="utf-8") as file:
        json.dump(books, file, indent=2, ensure_ascii=False)
    print(f"Daten erfolgreich in {category}.json gespeichert.")

# Schließe den Webdriver
driver.quit()
