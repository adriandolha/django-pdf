import os
import argparse, sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_pdf.settings')
import django

django.setup()

from django.core.cache import cache
import datetime
import json
import uuid
from dataclasses import dataclass
from typing import List
import boto3
import pandas as pd
import random
from faker import Faker
from django_pdf.logger import LOGGER
from countryinfo import CountryInfo

RECURRENT_EXPENSES = ['food', 'gas_electricity', 'phone', 'internet', 'transport', 'apartment']


def faker_config():
    return {'food': {'amount_range': (-200, -50), 'entries_per_month': (20, 40)},
            'transport': {'amount_range': (-250, -100), 'entries_per_month': (1, 3)},
            'travel': {'amount_range': (-3000, -500), 'entries_per_month': (0, 1)},
            'gas_electricity': {'amount_range': (-1000, -600), 'entries_per_month': (1, 1)},
            'internet': {'amount_range': (-55, -30), 'entries_per_month': (1, 1)},
            'phone': {'amount_range': (-300, -120), 'entries_per_month': (1, 1)},
            'apartment': {'amount_range': (-800, -200), 'entries_per_month': (0, 1)},
            'health': {'amount_range': (-200, -50), 'entries_per_month': (0, 3)}}


# COUNTRIES = list(CountryInfo().all().keys())
COUNTRIES = ['Netherlands',
             'Iceland',
             'Spain',
             'Portugal',
             'Italy',
             'France',
             'Romania',
             'United Kingdom',
             'Ireland',
             'Russia',
             'Malta',
             'Germany',
             'Greece',
             'Cuba',
             'China',
             'Japan',
             'United States',
             'Canada',
             'Mexico',
             'Egypt',
             'Morocco',
             'Czech Republic',
             'Senegal']


@dataclass
class Category:
    name: str
    key_words: list[str]

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data: dict):
        return Category(**data)

    def __eq__(self, other):
        return self.name == other.name if other else False


def get_all_dates_grouped_by_year_and_month(delta_days: int):
    today = datetime.datetime.today()
    dates_by_year_and_month = {}
    for days in range(0, delta_days):
        previous_date = today - datetime.timedelta(days=days)
        year_month = f'{previous_date.year}-{previous_date.month}'
        if not dates_by_year_and_month.get(year_month):
            dates_by_year_and_month[year_month] = []
        date = f'{year_month}-{previous_date.day}'
        dates_by_year_and_month[year_month].append(date)
    return dates_by_year_and_month


def random_country():
    return COUNTRIES[random.randint(0, len(COUNTRIES) - 1)]


def get_countries():
    return COUNTRIES


def create_user_data(username, country, categories: List[Category], destination_file: str, years: int = 1):
    _faker = Faker()
    _faker_config = faker_config()
    categories_by_name = {category.name: category.key_words for category in categories}
    data = []
    dates = get_all_dates_grouped_by_year_and_month(365 * years)
    for year_and_month in dates.keys():
        for category_name in _faker_config.keys():
            for i in range(0, random.randint(*_faker_config[category_name]['entries_per_month'])):
                date = random.choice(dates[year_and_month])
                key_word = random.choice(categories_by_name[category_name])
                _text = _faker.text(max_nb_chars=random.randint(100, 300))
                desc = f'{key_word} {_text}'
                amount = random.randint(*_faker_config[category_name]['amount_range'])
                data.append([username, country, date, desc, amount, category_name])

    df = pd.DataFrame(columns=['username', 'country', 'date', 'desc', 'amount', 'category'], data=data)
    df.to_json(destination_file)


def create_users_data(no_of_users, destination_path: str, categories_file: str, years: int = 1):
    LOGGER.info(f'Loading categories from {categories_file} ')
    categories = [Category.from_dict(category) for category in json.load(open(categories_file))]
    LOGGER.debug(categories)
    for i in range(1, no_of_users + 1):
        country = random_country()
        username = f'user{i}'
        destination_file = f'{destination_path}/{username}.json'
        LOGGER.info(
            f'Create user data for user {username}, country {country}, in destination {destination_path} for {years} '
            f'year(s) banks statements data.')
        create_user_data(username, country, categories, destination_file, years)


def expenses_per_month(df: pd.DataFrame, additional_filters=lambda df: df):
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month'] = pd.DatetimeIndex(df['date']).month
    df = df.groupby(['username', 'country', 'year', 'month'], as_index=False).sum()
    df['amount'] = df['amount'].round().abs().astype(int)
    df = additional_filters(df)

    result = {'columns': df.columns.values.tolist(), 'items': df.values.tolist()}
    return result


def avg_expenses_per_category(df: pd.DataFrame, additional_filters=lambda df: df):
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month'] = pd.DatetimeIndex(df['date']).month
    df = df.groupby(['username', 'country', 'category', 'year', 'month'], as_index=False).sum()
    df['amount'] = df['amount'].round().abs().astype(int)
    df = df.groupby(['username', 'country', 'category'], as_index=False)['amount'].mean()
    df['amount'] = df['amount'].round().abs().astype(int)
    df = additional_filters(df)
    # LOGGER.info(f"Return result...")
    # LOGGER.debug(df.to_string())
    return {'columns': df.columns.values.tolist(), 'items': df.values.tolist()}


def create_reports(path: str):
    TTL = 3600 * 24 * 7
    df_paths = [os.path.join(path, file) for file in os.listdir(path)]
    print(df_paths)
    dfs = [pd.read_json(file) for file in df_paths[0:3] if file.endswith('.json')]
    _df = pd.concat(dfs, ignore_index=True)
    users = _df['username'].unique().tolist()
    print(users)

    def admin_expenses_per_month(df_: pd.DataFrame):
        _df = df_.groupby(['country', 'year', 'month'], as_index=False)['amount'].mean()
        _df['amount'] = _df['amount'].round().abs().astype(int)
        return _df

    def admin_avg_expenses_per_category(df_: pd.DataFrame):
        _df = df_.groupby(['country', 'category'], as_index=False)['amount'].mean()
        _df['amount'] = _df['amount'].round().abs().astype(int)
        return _df

    for username in users:
        q = f"username == '{username}'"
        LOGGER.info(q)
        # _expenses_per_month = expenses_per_month(_df.copy(), lambda df_: df_.query(q))
        # _avg_expenses_per_category = avg_expenses_per_category(_df.copy(), lambda df_: df_.query(q))
        # LOGGER.info(_expenses_per_month)

    _expenses_per_month = expenses_per_month(_df.copy(), admin_expenses_per_month)
    cache.set(f'admin#reports#expenses_per_month', json.dumps(_expenses_per_month), timeout=TTL)
    # LOGGER.info(_expenses_per_month)
    _avg_expenses_per_category = avg_expenses_per_category(_df.copy(), admin_avg_expenses_per_category)
    cache.set(f'admin#reports#avg_expenses_per_category', json.dumps(_avg_expenses_per_category), timeout=TTL)
    # LOGGER.info(_avg_expenses_per_category)
