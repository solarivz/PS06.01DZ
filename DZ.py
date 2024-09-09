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
    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="product-card"]')))
except TimeoutException:
    print("Элементы не были найдены в течение заданного времени")
    driver.quit()
    exit()

parsed_data = []

# Перебираем каждую карточку товара
for product in products:
    try:
        # Извлекаем информацию о товаре
        title = product.find_element(By.XPATH, './/span[@itemprop="name"]').text
        price = product.find_element(By.XPATH, './/meta[@itemprop="price"]').get_attribute('content')
        #link = product.find_element(By.XPATH, './/a[@class="ui-GPFV8 XGLam"]').get_attribute('href')
        link = product.find_element(By.XPATH, './/a[contains(@class, "ui-GPFV8")]').get_attribute('href')

        # Проверяем наличие производителя, если доступно
        try:
            manufacturer = product.find_element(By.XPATH, './/div[contains(@class, "manufacturer-class")]').text
        except NoSuchElementException:
            manufacturer = "Не указан"

        parsed_data.append([title, manufacturer, price, link])
    except NoSuchElementException as e:
        print(f"Элемент не найден: {e}")
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")

# Закрываем браузер
driver.quit()

# Сохраняем данные в CSV-файл
with open("products.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название товара', 'Производитель', 'Цена', 'Ссылка на товар'])
    writer.writerows(parsed_data)

print(f"Собрано {len(parsed_data)} товаров")