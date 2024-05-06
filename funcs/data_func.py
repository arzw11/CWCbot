import sqlite3

connection = sqlite3.connect('cwc_database.db')
cursor = connection.cursor()

def get_data(value:str):
    cursor.execute(f'SELECT * FROM {value}')
    result = cursor.fetchall()

    return result
