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
    cursor.execute(f'SELECT {columns_joined} FROM {table}')
    rows = cursor.fetchall()
    result = []
    for i in rows:
        dict = {}
        for index, column in enumerate(columns):
            dict[column] = i[index]
        result.append(dict)


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f'DELETE FROM {table} WHERE id={row_id}')
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """ DB initialization"""
    with open('budget_db.sql', 'r') as f:
        init = f.read()
    cursor.executescript(init)
    conn.commit()


def check_db():
    """Check if DB exists and if its not- create it"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='expense'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db()