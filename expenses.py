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
    category_name: str


def _parse_message(raw_message: str) -> Message:
    """Parsing text about new expense"""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу распознать расход. Попробуйте написать в формате, "
            "например: \n 10 такси")
    amount = regexp_result.group(1).replace("", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount,category_text=category_text)