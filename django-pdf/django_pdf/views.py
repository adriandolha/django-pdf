import dataclasses
import json
import uuid

from django.core.cache import cache
from django.http import HttpResponse
from django.template import loader

from django_pdf import reportlab_pdf, REPORTS_CACHE_SOURCE
from django_pdf import selenium_pdf
from django_pdf import weasyprint_pdf
from django_pdf.auth import requires_permission
from django_pdf.logger import LOGGER
from django_pdf import seaborn_reports

TASK_ID = str(uuid.uuid4())
APP_LABEL = 'django_pdf'


@dataclasses.dataclass
class Reports:
    avg_expenses_per_category: dict
    avg_expenses_per_category_json: str
    expenses_per_month: dict
    expenses_per_month_json: str
    countries: list
    countries_json: str

    def to_dict(self):
        return self.__dict__


def get_from_cache(key):
    _key = key if REPORTS_CACHE_SOURCE == 'local' else f'{REPORTS_CACHE_SOURCE}#{key}'
    return cache.get(_key)


def get_all_reports():
    avg_expenses_per_category_json = get_from_cache(f'admin#reports#avg_expenses_per_category')
    avg_expenses_per_category = json.loads(avg_expenses_per_category_json)
    countries = list(set(map(lambda item: item[0], avg_expenses_per_category['items'])))
    LOGGER.debug(countries)

    expenses_per_month_json = get_from_cache(f'admin#reports#expenses_per_month')
    expenses_per_month = json.loads(expenses_per_month_json)
    # LOGGER.debug(avg_expenses_per_category_json)
    LOGGER.debug(expenses_per_month_json)
    return Reports(avg_expenses_per_category=avg_expenses_per_category,
                   avg_expenses_per_category_json=avg_expenses_per_category_json,
                   expenses_per_month=expenses_per_month,
                   expenses_per_month_json=expenses_per_month_json,
                   countries=countries,
                   countries_json=json.dumps(countries))


def view_expenses_chartsjs(request):
    template = loader.get_template('home.html')
    reports = get_reports_for_first_country()
    LOGGER.debug('Reports for first country...')
    LOGGER.debug(reports.expenses_per_month)
    rendered_template = template.render({'charts': 'chartsjs', **reports.to_dict()}, request)
    # LOGGER.debug(rendered_template)
    return rendered_template


def get_reports_for_first_country():
    reports = get_all_reports()
    reports.avg_expenses_per_category['items'] = list(filter(lambda item: item[0] == reports.countries[0],
                                                             reports.avg_expenses_per_category['items']))
    countries = list(set(map(lambda item: item[0], reports.expenses_per_month['items'])))

    reports.expenses_per_month['items'] = list(filter(lambda item: item[0] == countries[0],
                                                      reports.expenses_per_month['items']))
    return reports


def view_expenses_seaborn(request):
    template = loader.get_template('home.html')
    reports = get_all_reports()
    reports.avg_expenses_per_category['items'] = filter(lambda item: item[0] == reports.countries[0],
                                                        reports.avg_expenses_per_category['items'])
    reports.expenses_per_month['items'] = filter(lambda item: item[0] == reports.countries[0],
                                                 reports.expenses_per_month['items'])

    _seaborn_reports = seaborn_reports.get_all_reports()

    rendered_template = template.render({'charts': 'seaborn', **_seaborn_reports.to_dict(), **reports.to_dict()},
                                        request)
    # LOGGER.debug(rendered_template)
    return rendered_template


@requires_permission([f'{APP_LABEL}.view_report'])
def home(request):
    pdf_data = None
    LOGGER.debug(f'charts={request.GET.get("charts")}')
    is_chartsjs = request.GET.get('charts') and request.GET.get('charts') == 'chartsjs'
    LOGGER.debug(f'is_chartsjs={is_chartsjs}')

    view_expenses = lambda request: view_expenses_chartsjs(request) if is_chartsjs else view_expenses_seaborn(request)
    if request.GET.get('download') and request.GET.get('download') == 'weasyprint':
        pdf_data = weasyprint_pdf.get_pdf(view_expenses(request))

    if request.GET.get('download') and request.GET.get('download') == 'reportlab':
        pdf_data = reportlab_pdf.get_pdf(get_reports_for_first_country())

    if request.GET.get('download') and request.GET.get('download') == 'selenium':
        pdf_data = selenium_pdf.get_pdf(request.GET.get('url'))
    if pdf_data:
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="report.pdf"'
        return response

    return HttpResponse(view_expenses(request))


def health(request):
    return HttpResponse("OK")
