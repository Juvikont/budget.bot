"""Expenses- CRUD and stats"""
import datetime
import re
from typing import NamedTuple

import pytz

import db
import exceptions
from categories import Categories



class Message(NamedTuple):
    """Unparsed message structure"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """Newly added expense structure"""
    amount: int
    codename: str



def _parse_message(raw_message: str) -> Message:
    """Parsing text about new expense"""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу распознать расход. Попробуйте написать в формате, "
            "например: \n 10 такси")
    amount = int(regexp_result.group(1).replace("", ""))
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_datetime():
    """Returns today datetime in Warsaw timezone"""
    timezone = pytz.timezone("Europe/Warsaw")
    now = datetime.datetime.now(timezone)
    return now


def _get_date_formatted() -> str:
    """ Returns nowadate as string"""
    return _get_now_datetime().strftime("%Y-%m-%d")


def _get_budget_limit() -> int:
    """Returns daily lime for main bases expenses"""
    return db.fetchall("budget", ["daily_limit"])[0]["daily_limit"]


def delete_expense(row_id: str) -> None:
    """Delete msg by its id"""
    db.delete("expense", row_id)


def add_expense(raw_message: str, chat_id: int) -> Expense:
    """Adding new expense from bot msg"""
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(parsed_message.category_text)
    db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_date_formatted(),
        "codename": category.name,
        "raw_text": raw_message,
        "chat_id": chat_id
    })
    return Expense(amount=parsed_message.amount,
                   codename=category.name)


def get_today_statistics(chat_id: int) -> str:
    """Returns todays statistics as string"""
    cursor = db.get_cursor()
    chat = int(chat_id)
    cursor.execute((
        "SELECT sum(amount)"
        "FROM expense WHERE created=current_date and chat_id =:chat"),{'chat': chat})
    result = cursor.fetchone()
    if not result[0]:
        return "Сегодня ещё нет расходов"
    all_today_expenses = result[0]
    # Base expenses
    cursor.execute((
        "SELECT sum(amount)"
        "FROM expense WHERE created=current_date and chat_id =:chat  "
        "AND codename IN "
        "(SELECT name FROM category "
        "WHERE is_base_expense = true )"),{'chat': chat})
    result = cursor.fetchone()
    print(result)
    main_today_expenses = result[0] if result[0] else 0
    other_expenses = str(all_today_expenses - main_today_expenses)
    return (
        f"Сегодняшние расходы: \n"
        f"Всего - {all_today_expenses} zl.\n"
        f"Основные - {main_today_expenses} zl. из {_get_budget_limit()} zl. \n\n"
        f"Прочие - {other_expenses}")


def last(chat_id: int):
    """Возвращает последние несколько расходов"""
    cursor = db.get_cursor()
    chat = int(chat_id)
    cursor.execute((
        "select e.id, e.amount,c.name,e.chat_id "
        "from expense e left join category c "
        "on c.name=e.codename where e.chat_id = :chat  "
        "order by created  desc limit 10"),{'chat': chat})
    rows = cursor.fetchall()
    print(chat)
    last_expenses = []
    for row in rows:
        last_expenses.append({
            'amount': row[1],
            'id': row[0],
            'codename': row[2]
        })
    return last_expenses

sum1 = Expense(amount=3,codename='black')
print(sum1.amount)