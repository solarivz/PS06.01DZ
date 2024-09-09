from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
import csv
import time

# Инициализация WebDriver для Chrome
driver = webdriver.Chrome()

# Указываем URL сайта с вакансиями
url = "https://tomsk.hh.ru/vacancies/programmist"
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

# Ждём, пока все карточки с вакансиями не появятся
try:
    vacancies = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'vacancy-serp-item')))
except TimeoutException:
    print("Элементы не были найдены в течение заданного времени")
    driver.quit()
    exit()

parsed_data = []

# Перебираем каждую карточку вакансии
for vacancy in vacancies:
    try:
        # Используем XPath для точного извлечения информации
        title = vacancy.find_element(By.XPATH, './/a[contains(@data-qa, "serp-item__title")]').text
        company = vacancy.find_element(By.XPATH, './/a[contains(@data-qa, "vacancy-serp__vacancy-employer")]').text
        salary = vacancy.find_element(By.XPATH, './/span[contains(@data-qa, "vacancy-serp__vacancy-compensation")]').text
        link = vacancy.find_element(By.XPATH, './/a[contains(@data-qa, "serp-item__title")]').get_attribute('href')
        parsed_data.append([title, company, salary, link])
    except NoSuchElementException as e:
        print(f"Элемент не найден: {e}")
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")

# Закрываем браузер
driver.quit()

# Сохраняем данные в CSV-файл
with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'название компании', 'зарплата', 'ссылка на вакансию'])
    writer.writerows(parsed_data)

print(f"Собрано {len(parsed_data)} вакансий")
