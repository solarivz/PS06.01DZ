from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
import csv

# Инициализация WebDriver для Firefox
driver = webdriver.Firefox()
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)

# Инициализация WebDriverWait с ожиданием до 10 секунд
wait = WebDriverWait(driver, 10)

# Ждём, пока все карточки с вакансиями не появятся
try:
    vacancies = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'vacancy-serp__results')))
except TimeoutException:
    print("Элементы не были найдены в течение заданного времени")
    driver.quit()
    exit()

parsed_data = []

for vacancy in vacancies:
    try:
        # Использование XPath для поиска нужных элементов
        title = vacancy.find_element(By.XPATH, './/a[contains(@data-qa, "vacancy-serp__vacancy-title")]').text
        company = vacancy.find_element(By.XPATH, './/a[contains(@data-qa, "vacancy-serp__vacancy-employer")]').text
        salary = vacancy.find_element(By.XPATH, './/span[contains(@data-qa, "vacancy-serp__vacancy-compensation")]').text
        link = vacancy.find_element(By.XPATH, './/a[contains(@data-qa, "vacancy-serp__vacancy-title")]').get_attribute('href')
        parsed_data.append([title, company, salary, link])
    except NoSuchElementException as e:
        print(f"Элемент не найден: {e}")
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")

driver.quit()

# Сохранение данных в CSV
with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'название компании', 'зарплата', 'ссылка на вакансию'])
    writer.writerows(parsed_data)
