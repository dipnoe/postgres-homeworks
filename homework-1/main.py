"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv
import os

KEYS = ('customers', 'employees', 'orders')
PASSWORD: str = os.getenv('PASSWORD')

# поля, не включающие автоинкремент
employees_fields = '("first_name", "last_name", "title", "birth_date", "notes")'


def get_value(key):
    """
    Шаблоны для плейсхолдеров
    """
    if key == 'customers':
        return '(%s, %s, %s)'
    if key == 'employees':
        return '(%s, %s, %s, %s, %s)'
    return '(%s, %s, %s, %s, %s)'


def get_path(key) -> str:
    file_path = f'north_data/{key}_data.csv'
    return file_path


def csv_reader(csv_file: str):
    """
    Чтение csv файла и получение данных из него
    """
    with open(csv_file, 'r', encoding='utf-8') as file_:
        data = list(csv.reader(file_))
        return data[1:]


def connect_to_db(db_name):
    conn = psycopg2.connect(
        host='localhost',
        database=db_name,
        user='postgres',
        password=PASSWORD
    )
    return conn


def insert_query(file_csv, key, value, fields=''):
    """
    Вставка данных из файла в таблицу базы данных
    """
    try:
        with connect_to_db('north') as conn:
            with conn.cursor() as cursor:
                query = f'INSERT INTO {key} {fields} VALUES {value}'
                cursor.executemany(query, file_csv)

    finally:
        conn.close()


if __name__ == '__main__':
    for key_ in KEYS:
        file = csv_reader(get_path(key_))

        if key_ == 'employees':
            insert_query(file, key_, get_value(key_), fields=employees_fields)
        else:
            insert_query(file, key_, get_value(key_))
