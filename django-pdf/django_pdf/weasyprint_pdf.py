from weasyprint import HTML

from django_pdf.logger import LOGGER


def get_pdf(html):
    LOGGER.debug('Generating pdf...')
    pdf_data = HTML(string=html).write_pdf()
    LOGGER.debug('Generated pdf.')
    return pdf_data