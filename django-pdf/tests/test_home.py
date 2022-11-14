from unittest import mock
from unittest.mock import patch, MagicMock

from django.test import Client, RequestFactory
from django_pdf import views


class TestHome:
    def test_home_unauthorized(self):
        client = Client()
        response = client.get('/')
        assert response.status_code == 302

    def test_home_valid(self, cache_mock):
        request = MagicMock()
        res = views.home(request)
        assert res.status_code == 200

    def test_home_weasyprint_valid(self, cache_mock, weasyprint_mock):
        request = MagicMock()
        request.GET = {'download': 'weasyprint'}
        res = views.home(request)
        assert res.status_code == 200
        assert weasyprint_mock.return_value.write_pdf.called

    def test_home_selenium_valid(self, cache_mock, selenium_webdriver_mock):
        request = MagicMock()
        request.GET = {'download': 'selenium'}
        res = views.home(request)
        assert res.status_code == 200
        assert selenium_webdriver_mock.execute_cdp_cmd.called
        selenium_webdriver_mock.get.assert_called_once_with('http://localhost:8000/')

    def test_home_selenium_custom_url(self, cache_mock, selenium_webdriver_mock):
        request = MagicMock()
        request.GET = {'download': 'selenium', 'url': 'http://example.com'}
        res = views.home(request)
        assert res.status_code == 200
        assert selenium_webdriver_mock.execute_cdp_cmd.called
        selenium_webdriver_mock.get.assert_called_once_with('http://example.com')

    def test_home_reportlab_valid(self, cache_mock, reportlab_mock):
        request = MagicMock()
        request.GET = {'download': 'reportlab'}
        res = views.home(request)
        assert res.status_code == 200
        assert reportlab_mock.return_value.build.called
        assert len(reportlab_mock.return_value.build.call_args.args[0]) == 6

    @mock.patch('django_pdf.views.view_expenses_chartsjs')
    @mock.patch('django_pdf.views.view_expenses_seaborn')
    def test_home_charts_query_param_chartsjs_valid(self, view_seaborn, view_chartsjs, cache_mock):
        request = MagicMock()
        request.GET = {'charts': 'chartsjs'}
        res = views.home(request)
        assert res.status_code == 200
        assert view_chartsjs.called
        assert not view_seaborn.called

    @mock.patch('django_pdf.views.view_expenses_chartsjs')
    @mock.patch('django_pdf.views.view_expenses_seaborn')
    def test_home_charts_query_param_seaborn_valid(self, view_seaborn, view_chartsjs, cache_mock):
        request = MagicMock()
        request.GET = {'charts': 'seaborn'}
        res = views.home(request)
        assert res.status_code == 200
        assert view_seaborn.called
        assert not view_chartsjs.called

    @mock.patch('django_pdf.views.view_expenses_chartsjs')
    @mock.patch('django_pdf.views.view_expenses_seaborn')
    def test_home_charts_query_param_default(self, view_seaborn, view_chartsjs, cache_mock):
        request = MagicMock()
        res = views.home(request)
        assert res.status_code == 200
        assert not view_chartsjs.called
        assert view_seaborn.called
