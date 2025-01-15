import sqlite3
import csv
from dataclasses import fields
from datetime import datetime
import chardet
import pandas as pd
# Путь к CSV-файлам
vacancies_csv_file = 'vacancies_2024.csv'
currency_csv_file = 'currency.csv'
# Создание/подключение к SQLite базе данных
conn = sqlite3.connect('database.sqlite3')
cursor = conn.cursor()
# Создание таблицы с avg_salary и переведенной зарплатой в рубли
cursor.execute('''
CREATE TABLE IF NOT EXISTS job_vacancies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    key_skills TEXT,
    avg_salary REAL,
    salary_currency TEXT,
    salary_in_rub REAL,
    area_name TEXT,
    published_at TEXT
)
''')
# Загрузка курсов валют из файла currency.csv
currency_rates = {}
with open(currency_csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        date = row['date']
        currency_rates[date] = {
            'RUR': float(row['RUR']) if row['RUR'] else None,
            'BYR': float(row['BYR']) if row['BYR'] else None,
            'USD': float(row['USD']) if row['USD'] else None,
            'EUR': float(row['EUR']) if row['EUR'] else None,
            'KZT': float(row['KZT']) if row['KZT'] else None,
            'UAH': float(row['UAH']) if row['UAH'] else None,
            'AZN': float(row['AZN']) if row['AZN'] else None,
            'KGS': float(row['KGS']) if row['KGS'] else None,
            'UZS': float(row['UZS']) if row['UZS'] else None,
            'GEL': float(row['GEL']) if row['GEL'] else None
        }
# Открытие и чтение CSV-файла с вакансиями
with open(vacancies_csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    # Вставка данных в таблицу
    for row in csv_reader:
        salary_from = float(row['salary_from']) if row['salary_from'] else None
        salary_to = float(row['salary_to']) if row['salary_to'] else None
        # Вычисление среднего значения зарплаты
        if salary_from is not None and salary_to is not None:
            avg_salary = (salary_from + salary_to) / 2
        elif salary_from is not None:
            avg_salary = salary_from
        elif salary_to is not None:
            avg_salary = salary_to
        else:
            avg_salary = None
        # Получение курса валюты на дату публикации вакансии
        published_date = row['published_at'].split()[0][:7]  # Приводим дату к формату "YYYY-MM"
        currency = row['salary_currency'].upper()  # Приводим валюту к верхнему регистру
        # Проверка наличия курса валюты для данной даты
        if published_date in currency_rates and currency in currency_rates[published_date]:
            rate_to_rub = currency_rates[published_date][currency]
        else:
            rate_to_rub = None
            # Рассчитываем зарплату в рублях
        if rate_to_rub is not None:
            salary_in_rub = avg_salary * rate_to_rub if avg_salary is not None else None
            if salary_in_rub and salary_in_rub > 10000000:  # Ограничение на максимальную зарплату
                salary_in_rub = None
        else:
            salary_in_rub = None
        cursor.execute('''
        INSERT INTO job_vacancies (
            name, key_skills, avg_salary, salary_currency, salary_in_rub, area_name, published_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['name'],
            row['key_skills'],
            avg_salary,
            row['salary_currency'],
            salary_in_rub,
            row['area_name'],
            row['published_at']
        ))
# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
print("Данные успешно импортированы в базу данных с конвертацией в рубли!")