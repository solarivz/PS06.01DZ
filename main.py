from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
import csv
import time

# Инициализация WebDriver для Firefox
# driver = webdriver.Firefox()
# Если мы используем Chrome, пишем
driver = webdriver.Chrome()



url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)

# Прокручиваем страницу вниз для подгрузки всех элементов
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)  # Ждем загрузки контента

# Инициализация WebDriverWait с увеличенным временем ожидания
wait = WebDriverWait(driver, 20)

# Ждём, пока все карточки с вакансиями не появятся
try:
    vacancies = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@class, "magritte-grid-layout-content___fzkS0_2-1-10")]')))
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


# Прописываем открытие нового файла, задаём ему название и форматирование
# 'w' означает режим доступа, мы разрешаем вносить данные в таблицу
with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    # Используем модуль csv и настраиваем запись данных в виде таблицы
    # Создаём объект
    writer = csv.writer(file)
    # Создаём первый ряд
    writer.writerow(['Название вакансии', 'название компании', 'зарплата', 'ссылка на вакансию'])

    # Прописываем использование списка как источника для рядов таблицы
    writer.writerows(parsed_data)

# Чтобы удобнее просмотреть результат, открываем файл через программу для чтения и редактирования таблиц.