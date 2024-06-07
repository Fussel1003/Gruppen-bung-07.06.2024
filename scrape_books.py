from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Webdriver initialisieren
driver = webdriver.Firefox()

# Öffne die Webseite
driver.get("http://books.toscrape.com")

# Initialisiere eine Liste, um die Daten zu speichern
books_data = []

# Schleife durch die Seiten der Webseite
while True:
    # Finde alle Bücher auf der aktuellen Seite
    books = driver.find_elements(By.CLASS_NAME, "product_pod")
    
    for book in books:
        # Finde den Titel
        title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
        
        # Finde den Preis
        price = book.find_element(By.CLASS_NAME, "price_color").text
        
        # Finde die Verfügbarkeit
        availability = book.find_element(By.CLASS_NAME, "availability").text.strip()
        
        # Füge die Buchdaten zur Liste hinzu
        books_data.append([title, price, availability])
    
    # Überprüfe, ob eine "Next"-Seite vorhanden ist
    try:
        next_button = driver.find_element(By.CLASS_NAME, "next")
        next_button.find_element(By.TAG_NAME, "a").click()
        time.sleep(2)  # Wartezeit, damit die nächste Seite geladen wird
    except:
        break  # Wenn keine "Next"-Seite vorhanden ist, breche die Schleife ab

# Schließe den Webdriver
driver.quit()

# Schreibe die Daten in eine CSV-Datei
with open("books_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Availability"])
    writer.writerows(books_data)

print("Daten erfolgreich in books_data.csv gespeichert.")
