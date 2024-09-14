from copy import deepcopy
from decimal import Decimal
from datetime import datetime, timedelta


CORRECT_COLLECT_CREATE_DATA = {
    'title': 'string',
    'slug': 'string',
    'occasion': 'string',
    'target_amount': Decimal('655519.30'),
    'end_datetime': (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
}

CORRECT_PARTIAL_UPDARE_DATA = {
    'title': 'string1',
    'slug': 'string2',
    'occasion': 'string3',
    'target_amount': Decimal('123.30'),
    'end_datetime': (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
}


class Incorrect_collect_create_data:
    correct_data = CORRECT_COLLECT_CREATE_DATA

    @classmethod
    def get_incorrect_end_datetime(cls):
        incorrect_end_datetime = deepcopy(cls.correct_data)
        incorrect_end_datetime['end_datetime'] = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        return incorrect_end_datetime

    @classmethod
    def get_incorrect_slug(cls):
        incorrect_slug = deepcopy(cls.correct_data)
        incorrect_slug['slug'] = '.1.1.1.'
        return incorrect_slug

    @classmethod
    def get_incorrect_target_amount(cls):
        incorrect_target_amount = deepcopy(cls.correct_data)
        incorrect_target_amount['target_amount'] = Decimal('-1')
        return incorrect_target_amount
