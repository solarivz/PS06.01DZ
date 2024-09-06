from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
import csv

# Инициализация WebDriver для Firefox
driver = webdriver.Firefox()
# В отдельной переменной указываем сайт, который будем просматривать
url = "https://tomsk.hh.ru/vacancies/programmist"

# Открываем веб-страницу
driver.get(url)


# Инициализация WebDriverWait с ожиданием до 10 секунд
wait = WebDriverWait(driver, 10)

# Ждём, пока все карточки с вакансиями не появятся
try:
    vacancies = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'vacancy-info--I4f9shQE53f9Luf5lkMw')))
except TimeoutException:
    print("Элементы не были найдены в течение заданного времени")
    driver.quit()
    exit()

parsed_data = []

for vacancy in vacancies:
    try:
        # Находим элементы внутри вакансии
        title = vacancy.find_element(By.CSS_SELECTOR, 'span.vacancy-name-wrapper--R9iuXWkZt3U_qpqlrtC5').text
        company = vacancy.find_element(By.CSS_SELECTOR, 'span.company-info-text--O32pGCRW0YDmp3BHuNOP').text
        salary = vacancy.find_element(By.CSS_SELECTOR, 'span.compensation-text--cCPBXayRjn5GuLFWhGTJ').text
        link = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link').get_attribute('href')
        parsed_data.append([title, company, salary, link])
    except NoSuchElementException as e:
        print(f"Элемент не найден: {e}")
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")

driver.quit()

with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'название компании', 'зарплата', 'ссылка на вакансию'])
    writer.writerows(parsed_data)
