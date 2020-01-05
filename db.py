import os
from typing import Dict, Tuple, List

import sqlite3

conn = sqlite3.connect(os.path.join("db", "budget.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ', '.join('?' * len(column_values.keys()))
    cursor.executemany(
        f"INSERT {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ', '.join(columns)
    cursor.execute(f'SELECT{columns_joined}FROM{table}')
    rows = cursor.fetchall()
    result = []
    for i in rows:
        dict = {}
        for index, column in enumerate(columns):
            dict[column] = i[index]
        result.append(dict)

def get_cursor():
    return cursor

def _init_db():
    with open('budget_db.sql','r') as f:
        init = f.read()