import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
def run():
    conn = sqlite3.connect('database.sqlite3')
    # Выполнение первого SQL-запроса
    query_avg_salary = """
        SELECT
            SUBSTR(published_at, 1, 4) AS 'Год',
            ROUND(AVG(salary_in_rub),2) AS 'Средняя з/п'
        FROM job_vacancies
        GROUP BY SUBSTR(published_at, 1, 4)
        ORDER BY SUBSTR(published_at, 1, 4)
        """
    df_avg_salary = pd.read_sql_query(query_avg_salary, conn)
    # Выполнение второго SQL-запроса
    query_avg_salary_test = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        ROUND(AVG(salary_in_rub),2)  AS 'Средняя з/п для Программиста Python'
    FROM job_vacancies
    WHERE 
        name LIKE '%Python-программист%'
        OR name LIKE '%python%'
        OR name LIKE '%питон%'
        OR name LIKE '%пайтон%'
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4)
    """
    df_avg_salary_test = pd.read_sql_query(query_avg_salary_test, conn)
    # Закрытие соединения с базой данных
    conn.close()
    # Создание директории, если она отсутствует
    output_dir = "E:/программирую по приколу/pythonProject3/instance/media/uploads/2025/01/14"
    # Создание графика для всех вакансий
    fig_avg_salary, ax_avg_salary = plt.subplots()
    ax_avg_salary.plot(df_avg_salary['Год'], df_avg_salary['Средняя з/п'], label='Средняя зарплата', marker='o')
    ax_avg_salary.set_title('Средняя зарплата по годам для всех вакансий')
    ax_avg_salary.legend()
    ax_avg_salary.grid(axis='y')
    plt.xticks(rotation=60)
    # Сохранение графика для всех вакансий
    fig_avg_salary.savefig(os.path.join(output_dir, "all_vacancies_avg_salary_by_year.png"))
    plt.close(fig_avg_salary)
    print("График всех вакансий сохранен.")
    # Создание графика для вакансий Тестировщика
    fig_avg_salary_test, ax_avg_salary_test = plt.subplots()
    ax_avg_salary_test.plot(df_avg_salary_test['Год'], df_avg_salary_test['Средняя з/п для Программиста Python'],
                               label='Средняя зарплата', marker='o')
    ax_avg_salary_test.set_title('Средняя зарплата по годам для Программиста Python')
    ax_avg_salary_test.legend()
    ax_avg_salary_test.grid(axis='y')
    # Поворот меток оси x
    plt.xticks(rotation=60)
    # Сохранение графика для вакансий Тестировщика
    fig_avg_salary_test.savefig(os.path.join(output_dir, "python_vacancies_avg_salary_by_year.png"))
    plt.close(fig_avg_salary_test)
    print("График вакансий Программиста Python сохранен.")
run()