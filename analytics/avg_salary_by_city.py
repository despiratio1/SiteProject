import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def run():
    conn = sqlite3.connect('database.sqlite3')
    query_all = """
    SELECT
        area_name AS 'City',
        ROUND(AVG(salary_in_rub), 2) AS 'salary_by_area'
    FROM job_vacancies
    GROUP BY area_name
    HAVING CAST(COUNT(*) AS REAL) >= 
        ((SELECT COUNT(*) FROM job_vacancies)/100)
    ORDER BY ROUND(AVG(salary_in_rub), 2) DESC
    LIMIT 15
    """
    df_all = pd.read_sql_query(query_all, conn)
    # Выполнение второго SQL-запроса
    query_test = """
        SELECT
            area_name AS 'Город',
            ROUND(AVG(salary_in_rub), 2) AS 'Уровень зарплат по городам для Программиста Python'
        FROM job_vacancies
        WHERE 
            name LIKE '%Python-программист%'
            OR name LIKE '%python%'
            OR name LIKE '%питон%'
            OR name LIKE '%пайтон%'
        GROUP BY area_name
        ORDER BY ROUND(AVG(salary_in_rub), 2) DESC
        LIMIT 15 
    """
    df_test = pd.read_sql_query(query_test, conn)
    # Закрытие соединения с базой данных
    conn.close()
    output_dir = "E:/программирую по приколу/pythonProject3/instance/media/uploads/2025/01/14"
    # Создание графика для всех вакансий
    fig_geography, ax = plt.subplots()
    cities = np.arange(len(df_all['City']))
    ax.barh(y=cities, width=df_all['salary_by_area'], height=0.4, label='Уровень зарплат')
    ax.set_title('Средняя зарплата по годам для всех вакансий')
    ax.set_yticks(cities)
    ax.set_yticklabels(df_all['City'], fontsize=6)
    ax.legend()
    ax.grid(axis='x')
    fig_geography.savefig(os.path.join(output_dir, "geography_salary_by_city_all.png"))
    plt.close(fig_geography)
    print("График всех вакансий сохранен.")
    # Создание графика для вакансий тестировщика
    fig_geography_test, ax_test = plt.subplots()
    cities = np.arange(len(df_test['Город']))
    ax_test.barh(y=cities, width=df_test['Уровень зарплат по городам для Программиста Python'], height=0.4, label='Уровень зарплат')
    ax_test.set_title('Средняя зарплата по годам для Программиста Python')
    ax_test.set_yticks(cities)
    ax_test.set_yticklabels(df_test['Город'], fontsize=6)
    ax_test.legend()
    ax_test.grid(axis='x')
    fig_geography_test.savefig(os.path.join(output_dir, "geography_salary_by_city_python.png"))
    plt.close(fig_geography_test)
    print("График Программиста Python сохранен.")
run()