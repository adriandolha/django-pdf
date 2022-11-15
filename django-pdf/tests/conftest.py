import base64
import json
from unittest import mock
from unittest.mock import patch

import pytest


def cache_get(key):
    if key == 'admin#reports#avg_expenses_per_category' or key == 'redshift#admin#reports#avg_expenses_per_category':
        return json.dumps(
            {
                'columns': ['country', 'category', 'amount'],
                'items': [['Italy', 'apartment', '200']]
            }
        )
    if key == 'admin#reports#expenses_per_month' or key == 'redshift#admin#reports#expenses_per_month':
        return json.dumps(
            {
                'columns': ['country', 'year', 'month', 'amount'],
                'items': [['Italy', '2022', '1', '10000']]
            }
        )
    return None


@pytest.fixture()
def cache_mock():
    with mock.patch('django_pdf.views.cache') as _cache:
        with mock.patch('django_pdf.seaborn_reports.cache') as _seaborn_cache:
            _cache.get.side_effect = cache_get
            _seaborn_cache.get.side_effect = cache_get
            yield _cache


@pytest.fixture()
def weasyprint_mock():
    with mock.patch('django_pdf.weasyprint_pdf.HTML') as _html:
        yield _html


@pytest.fixture()
def selenium_webdriver_mock():
    with mock.patch('django_pdf.selenium_pdf.webdriver') as _webdriver:
        with mock.patch('django_pdf.selenium_pdf.WebDriverWait'):
            with mock.patch('django_pdf.selenium_pdf.time'):
                _chrome_driver = _webdriver.Chrome.return_value
                _chrome_driver.execute_cdp_cmd.return_value = {"data": base64.b64encode(b"hi")}
                yield _chrome_driver


@pytest.fixture()
def reportlab_mock():
    with mock.patch('django_pdf.reportlab_pdf.get_doc') as _doc:
        with mock.patch('django_pdf.reportlab_pdf.seaborn_reports'):
            yield _doc
