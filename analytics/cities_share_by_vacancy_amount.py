import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
def create_pie(df, title, img_path):
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(df['Доля вакансий в %'], labels=None, startangle=90, autopct='',
                                      pctdistance=0.85)
    ax.axis('equal')
    ax.set_title(title)
    # Создание легенды с названиями городов
    legend_labels = df['Город']
    ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5), title='Города')
    # Скрытие текстовых меток на круговой диаграмме
    for text in texts + autotexts:
        text.set_visible(False)
    # Сохранение диаграммы
    fig.savefig(img_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {os.path.basename(img_path)}")
def run():
    conn = sqlite3.connect('database.sqlite3')
    query_all = """
        SELECT
            area_name AS 'Город',
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM job_vacancies), 2) AS 'Доля вакансий в %'
        FROM job_vacancies
        GROUP BY area_name
        ORDER BY COUNT(*) DESC
        LIMIT 15
    """
    df_all = pd.read_sql_query(query_all, conn)
    query_backend = """
        SELECT
            area_name AS 'Город',
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM job_vacancies), 3) AS 'Доля вакансий в %'
        FROM job_vacancies
        WHERE
            name LIKE '%Python-программист%'
            OR name LIKE '%python%'
            OR name LIKE '%питон%'
            OR name LIKE '%пайтон%'
        GROUP BY area_name
        ORDER BY COUNT(*) DESC
        LIMIT 15
    """
    df_backend = pd.read_sql_query(query_backend, conn)
    # Закрытие соединения с базой данных
    conn.close()
    output_dir = "E:/программирую по приколу/pythonProject3/instance/media/uploads/2025/01/14"
    create_pie(df_all, 'Доля вакансий по городам (все вакансии)',
               os.path.join(output_dir,'geography_pie_all.png'))
    create_pie(df_backend, 'Доля вакансий Программиста Python по городам',
               os.path.join(output_dir,'geography_pie_python.png'))
run()