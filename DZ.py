from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
import csv
import time

# Инициализация WebDriver для Chrome
driver = webdriver.Chrome()

# Указываем URL сайта с товарами
url = "https://www.divan.ru/category/svet"
driver.get(url)

# Увеличиваем время ожидания и выполняем прокрутку вниз постепенно
wait = WebDriverWait(driver, 20)
last_height = driver.execute_script("return document.body.scrollHeight")

# Прокручиваем страницу вниз, пока новые элементы загружаются
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Ждём несколько секунд для подгрузки элементов
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Ждём, пока все карточки с товарами не появятся
try:
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'LlPhw')))
except TimeoutException:
    print("Элементы не были найдены в течение заданного времени")
    driver.quit()
    exit()

parsed_data = []

# Перебираем каждую карточку товара
for product in products:
    try:
        # Используем корректный XPath для извлечения информации
        title = product.find_element(By.XPATH, './/div[contains(@class, "wYUX2")]').text
        price = product.find_element(By.XPATH, './/div[contains(@class, "q5Uds T7z9Z fxA6s")]').text
        #link = product.find_element(By.XPATH, './/a[contains(@class, "ui-GPFV8 qUioe ProductName ActiveProduct")]').get_attribute("href")

        parsed_data.append([title, price])
    except NoSuchElementException as e:
        print(f"Элемент не найден: {e}")
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")

# Закрываем браузер
driver.quit()

# Сохраняем данные в CSV-файл
with open("products.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название товара', 'Цена'])
    writer.writerows(parsed_data)

print(f"Собрано {len(parsed_data)} товаров")