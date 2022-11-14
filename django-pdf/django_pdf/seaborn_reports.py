import base64
import dataclasses
import json
from io import BytesIO

import seaborn as sns
import pandas as pd
from django.core.cache import cache
import matplotlib.pyplot as plt
import matplotlib

from django_pdf.logger import LOGGER

matplotlib.use('SVG')


@dataclasses.dataclass
class ReportsPng:
    avg_expenses_per_category_pie: str
    avg_expenses_per_category_multiline: str
    expenses_per_month_multiline: str

    def to_dict(self):
        return self.__dict__


def png(plot, name):
    plot_file = BytesIO()
    plot.savefig(plot_file, format='png')
    encoded_file = base64.b64encode(plot_file.getvalue()).decode('utf-8')
    return encoded_file


def png_to_file(plot, name):
    plot.savefig(f'{name}.png', format='png')


def avg_expenses_per_category_multiline(data: dict, process_figure=png):
    plt.figure()

    df = pd.DataFrame(columns=data['columns'], data=data['items'])
    plot = sns.lineplot(df, x="category", y="amount", hue="country")

    return process_figure(plot.figure, 'avg_expenses_per_category_multiline')


def avg_expenses_per_category_pie(data: dict, process_figure=png):
    plt.figure()
    pie, ax = plt.subplots(figsize=[10, 6])
    df = pd.DataFrame(columns=data['columns'], data=data['items'])
    country = data['items'][0][0]
    LOGGER.debug(data['items'])

    df = df.query(f'country == "{country}"')
    LOGGER.debug(country)

    data = df['amount'].values
    labels = df['category'].values
    LOGGER.debug(data)
    LOGGER.debug(labels)

    colors = sns.color_palette('pastel')[0:7]

    plt.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
    return process_figure(pie, 'avg_expenses_per_category_pie')


def expenses_per_month_multiline(data: dict, process_figure=png):
    plt.figure()
    fig, ax = plt.subplots(figsize=(6, 6))
    df = pd.DataFrame(columns=data['columns'], data=data['items'])
    df['date'] = df.apply(lambda row: f'{row.year}-{row.month}', axis=1)
    plot = sns.lineplot(df, x="date", y="amount", hue="country", ax=ax)
    for index, label in enumerate(plot.get_xticklabels()):
        if index % 2 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    plt.xticks(rotation=60)
    return process_figure(plot.figure, 'expenses_per_month_multiline')


def get_all_reports():
    avg_expenses_per_category = json.loads(cache.get(f'admin#reports#avg_expenses_per_category'))
    expenses_per_month = json.loads(cache.get(f'admin#reports#expenses_per_month'))

    return ReportsPng(
        avg_expenses_per_category_multiline=avg_expenses_per_category_multiline(avg_expenses_per_category),
        avg_expenses_per_category_pie=avg_expenses_per_category_pie(avg_expenses_per_category),
        expenses_per_month_multiline=expenses_per_month_multiline(expenses_per_month)
    )


def save_reports_to_file():
    avg_expenses_per_category = json.loads(cache.get(f'admin#reports#avg_expenses_per_category'))
    expenses_per_month = json.loads(cache.get(f'admin#reports#expenses_per_month'))
    avg_expenses_per_category_multiline(avg_expenses_per_category, process_figure=png_to_file)
    avg_expenses_per_category_pie(avg_expenses_per_category, process_figure=png_to_file)
    expenses_per_month_multiline(expenses_per_month, process_figure=png_to_file)
