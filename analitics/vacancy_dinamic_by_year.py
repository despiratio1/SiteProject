import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run():
    conn = sqlite3.connect('database.sqlite3')

    # Выполнение первого SQL-запроса
    query_all = """
        SELECT
            SUBSTR(published_at, 1, 4) AS 'Год',
            COUNT(*) AS 'Количество вакансий'
        FROM job_vacancies
        GROUP BY SUBSTR(published_at, 1, 4)
        ORDER BY SUBSTR(published_at, 1, 4)
        """

    df_all = pd.read_sql_query(query_all, conn)

    # Выполнение второго SQL-запроса
    query_test = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        COUNT(*) AS 'Количество вакансий для Программиста Python'
    FROM job_vacancies
    WHERE 
        name LIKE '%Python-программист%'
        OR name LIKE '%python%'
        OR name LIKE '%питон%'
        OR name LIKE '%пайтон%'
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4)
    """

    df_test = pd.read_sql_query(query_test, conn)

    # Закрытие соединения с базой данных
    conn.close()

    # Создание директории, если она отсутствует
    output_dir = "E:/программирую по приколу/pythonProject3/instance/media/uploads/2025/01/14"

    # Создание графика для всех вакансий
    fig_all, ax_all = plt.subplots()
    years_all = np.arange(len(df_all['Год']))
    ax_all.bar(x=years_all, height=df_all['Количество вакансий'], width=0.4, label='Количество вакансий')
    ax_all.set_title('Количество всех вакансий по годам')
    ax_all.set_xticks(years_all)
    ax_all.set_xticklabels(df_all['Год'], rotation=90, ha='center')
    ax_all.legend()
    ax_all.grid(axis='y')

    # Сохранение графика для всех вакансий
    fig_all.savefig(os.path.join(output_dir, "all_vacancies.png"))
    plt.close(fig_all)
    print("График всех вакансий сохранен.")

    # Создание графика для вакансий Тестировщика
    fig_test, ax_test = plt.subplots()
    years_test = np.arange(len(df_test['Год']))
    ax_test.bar(x=years_test, height=df_test['Количество вакансий для Программиста Python'], width=0.4, label='Количество вакансий')
    ax_test.set_title('Количество вакансий по годам для Программиста Python')
    ax_test.set_xticks(years_test)
    ax_test.set_xticklabels(df_test['Год'], rotation=90, ha='center')
    ax_test.legend()
    ax_test.grid(axis='y')

    # Сохранение графика для вакансий Тестировщика
    fig_test.savefig(os.path.join(output_dir, "python_vacancies.png"))
    plt.close(fig_test)
    print("График вакансий Программиста Python сохранен.")


run()