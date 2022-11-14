import io

from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from django_pdf.logger import LOGGER

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from django_pdf import seaborn_reports

METADATA = {'saved_reports': False}

PRIMARY_COLOR = colors.cadetblue
SECONDARY_COLOR = colors.blue


def get_pdf(reports):
    if not METADATA['saved_reports']:
        seaborn_reports.save_reports_to_file()
        METADATA['saved_reports'] = True
    buffer = io.BytesIO()
    doc = get_doc(buffer)

    elements = []
    LOGGER.debug('Generating pdf...')

    about_section(elements)
    expenses_per_category_section(elements, reports)
    expenses_per_month_section(elements, reports)
    doc.build(elements)
    return buffer.getvalue()


def about_section(elements):
    title = '<b>Django PDF</b>'

    p_title = Paragraph(title, style=ParagraphStyle(name='centered', alignment=TA_CENTER))
    metadata_table = Table([
        [Paragraph('<b>Author:</b>', style=ParagraphStyle(name='centered', alignment=TA_LEFT, fontSize=8)),
         Paragraph('Adrian Dolha',
                   style=ParagraphStyle(name='centered', alignment=TA_RIGHT, fontSize=8, textColor=SECONDARY_COLOR))],
        [Paragraph('<b>Date:</b>', style=ParagraphStyle(name='centered', alignment=TA_LEFT, fontSize=8)),
         Paragraph('11 Nov 2022',
                   style=ParagraphStyle(name='centered', alignment=TA_RIGHT, fontSize=8, textColor=SECONDARY_COLOR))],
        [Paragraph('<link href="https://github.com/adriandolha/django-pdf"><u>Github Repo</u></link>',
                   style=ParagraphStyle(name='centered', alignment=TA_CENTER, fontSize=8, textColor=SECONDARY_COLOR)),
         '']
    ])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, -1), (-1, -1), PRIMARY_COLOR),
        ('TEXTCOLOR', (-1, -1), (0, -2), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, -1), (-1, -1), SECONDARY_COLOR),
        ('SPAN', (0, -1), (-1, -1),)
    ]
    ))
    description = """
        Django PDF is a web app used to prove how to create PDF using different libraries: 
        <span backColor=yellow><i>weasyprint</i></span>,
        <span backColor=yellow><i>selenium</i></span>,
        <span backColor=yellow><i>selenium</i></span>.
        <br></br>
        <b>Some conclusions:</b><br></br>
            <span color=black size=8>1. Use weasyprint to create PDF from static content (HTML, CSS).</span><br></br>
            <span color=black>2. Use selenium to create PDF from dynamic content. It handles dynamic Javascript, 
            including React apps, Bootstrap, MUI and ChartsJS. It can also authenticate to external apps.</span><br></br>
            <span color=black>3. Use reportlab to create custom PDF from scratch. Probably the most powerful method, 
            but also the most complex one.</span><br></br>
 
    """
    skill = lambda text: Paragraph(text, style=ParagraphStyle(name='desc', alignment=TA_CENTER, fontSize=8,
                                                              backColor=colors.cadetblue, borderColor=colors.black,
                                                              borderPadding=1,
                                                              borderRadius=10, borderWidth=0.5))
    techstack_table = Table([[skill('python'), skill('django'), skill('weasyprint'), skill('selenium'),
                              skill('reportlab'), skill('seaborn')],
                             [skill('pandas'), skill('chartsjs'), skill('bootstrap5'), skill('postgres'),
                              skill('redis')]])

    description_table = Table([
        [Paragraph(description, style=ParagraphStyle(name='desc', alignment=TA_LEFT, fontSize=8))],
        [techstack_table]
    ])
    description_table.setStyle(TableStyle([]))
    data = [[p_title, ''],
            [metadata_table, description_table]]
    table = Table(data, colWidths=[140, 360])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (-1, 1), (-1, -1), SECONDARY_COLOR),
        ('SPAN', (0, 0), (-1, 0),)
    ]
    ))

    elements.append(table)


def expenses_per_category_section(elements, reports):
    img = png(name='avg_expenses_per_category_pie.png', width=1000, height=600, aspect=0.3)

    data = [[avg_expenses_per_category_table(reports), img]]
    table = Table(data, colWidths=[250, 250])
    # table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.green),
    #                            ('TEXTCOLOR', (-1, 1), (-1, -1), colors.blue)]))
    elements.append(section_title('Average Expenses per Category'))
    elements.append(table)


def section_title(title: str):
    title_table = Table([[Paragraph(title,
                                    style=ParagraphStyle(name='section_title', alignment=TA_CENTER,
                                                         fontSize=8,
                                                         backColor=colors.blue, textColor=colors.white,
                                                         borderColor=colors.black,
                                                         borderPadding=1,
                                                         borderRadius=10, borderWidth=0.5))]], colWidths=500)
    return title_table


def expenses_per_month_section(elements, reports):
    img = png(name='expenses_per_month_multiline.png', width=600, height=600, aspect=0.5)
    elements.append(section_title('Expenses per Month'))
    elements.append(expenses_per_month_table(reports))
    elements.append(img)


def get_doc(buffer):
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                            topMargin=1.5 * cm, bottomMargin=2.5 * cm)
    return doc


def png(name, width, height, aspect):
    img = Image(name, width=aspect * width, height=aspect * height)
    return img


def avg_expenses_per_category_table(reports):
    data = [map(lambda col: col.capitalize(), reports.avg_expenses_per_category['columns']),
            *reports.avg_expenses_per_category['items']]
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
                               ('TEXTCOLOR', (-1, 1), (-1, -1), SECONDARY_COLOR),
                               ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)]))
    return table


def expenses_per_month_table(reports):
    data = [map(lambda col: col.capitalize(), reports.expenses_per_month['columns']),
            *reports.expenses_per_month['items']]

    table = Table(data, colWidths=[200, 100, 100, 100], repeatRows=1)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
                               ('TEXTCOLOR', (-1, 1), (-1, -1), SECONDARY_COLOR),
                               ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)]))
    return table
