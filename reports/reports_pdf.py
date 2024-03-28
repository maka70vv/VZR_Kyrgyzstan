import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import LongTable, TableStyle, BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re


def pdf_generator_reports(policies, travel_agency, start_date):
    inc = 1
    pdfmetrics.registerFont(TTFont('TimesNewRoman', '/home/makarov/PycharmProjects/VZR/reports/pdf_fonts/TimesNewRoman.ttf'))

    filename = f'{travel_agency}-{datetime.datetime.now()}.pdf'
    filename = re.sub(r'\s+', '_', filename)

    # Создание документа
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=50,
        bottomMargin=80,
        showBoundary=False)

    elements = []

    styles = getSampleStyleSheet()
    style_right = styles['Normal']
    style_right.fontName = 'TimesNewRoman'
    style_right.alignment = 2  # Выравнивание по правому краю
    to_whom = Paragraph('Кому: ЗАО "Страховая Компания "Кыргызстан" ', style_right)
    from_whom = Paragraph(f"От кого: {travel_agency} {travel_agency.inn}", style_right)
    date = Paragraph(f"Дата: {datetime.date.today().strftime('%d-%m-%Y')}", style_right)
    elements.append(to_whom)
    elements.append(from_whom)
    elements.append(date)

    # Заголовок
    title_style = getSampleStyleSheet()["Title"]
    title_style.fontName = 'TimesNewRoman'  # Установка шрифта для заголовка
    title = Paragraph("Отчет о проданных полисах", title_style)
    title2 = Paragraph(f"За период с {start_date} по {datetime.date.today()}", title_style)
    elements.append(title)
    elements.append(title2)

    # Данные таблицы
    data = [["№", 'Клиент', 'Дата продажи', 'Данные полиса', 'Стоимость включая налоги (KGS)', 'Сумма комиссии'], ]

    for policy in policies:
        data.append([
            str(inc),
            f'{policy.last_name} {policy.first_name} {policy.customer_inn}',
            str(policy.sale_date),
            f'Территория страхования - {policy.territory_and_currency}\n'
            f'Дата начала действия -  {policy.start_date}\n'
            f'Дата окончания действия полиса - {policy.end_date}',
            str(policy.price_with_taxes_kgs),
            str(policy.commission_summ)
        ])
        inc += 1

    tableStyle = [
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]

    styleN = styles['Normal']
    styleN.wordWrap = 'CJK'

    styleN.fontName = 'TimesNewRoman'  # Установка загруженного шрифта

    data2 = [[Paragraph(cell, styleN) for cell in row] for row in data]

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')

    colwidths = [frame._width * 0.1]  # Устанавливаем ширину для первого столбца
    colwidths.extend([frame._width * 0.21 for _ in range(4)])

    t = LongTable(data2, colWidths=colwidths)
    t.setStyle(TableStyle(tableStyle))
    elements.append(t)

    template = PageTemplate(id='longtable', frames=frame)
    doc.addPageTemplates([template])
    doc.build(elements)
    return filename


def pdf_generator_invoices(policies, travel_agency, start_date):
    inc = 1
    total_profit = 0
    total_commission = 0
    pdfmetrics.registerFont(TTFont('TimesNewRoman', '/home/makarov/PycharmProjects/VZR/reports/pdf_fonts/TimesNewRoman.ttf'))

    filename = f'{travel_agency}-{datetime.datetime.now()}.pdf'
    filename = re.sub(r'\s+', '_', filename)

    # Создание документа
    doc = BaseDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=50,
        bottomMargin=80,
        showBoundary=False)

    elements = []

    styles = getSampleStyleSheet()
    style_right = styles['Normal']
    style_right.fontName = 'TimesNewRoman'
    style_right.alignment = 2  # Выравнивание по правому краю
    to_whom = Paragraph(f'Кому: {travel_agency}\n'
                        f' {travel_agency.inn}', style_right)
    from_whom = Paragraph('От кого: ЗАО "Страховая Компания "Кыргызстан" ', style_right)
    date = Paragraph(f"Дата: {datetime.date.today().strftime('%d-%m-%Y')}", style_right)
    elements.append(to_whom)
    elements.append(from_whom)
    elements.append(date)

    # Заголовок
    title_style = getSampleStyleSheet()["Title"]
    title_style.fontName = 'TimesNewRoman'  # Установка шрифта для заголовка
    title = Paragraph("Счет на оплату", title_style)
    title2 = Paragraph(f"На основании отчета о проданных полисах за период с {start_date} по {datetime.date.today()}", title_style)
    elements.append(title)
    elements.append(title2)

    # Данные таблицы
    data = [["№", 'Клиент', 'Дата продажи', 'К оплате (за вычетом комиссии и налогов)', 'Сумма комиссии'], ]

    for policy in policies:
        data.append([
            str(inc),
            f'{policy.last_name} {policy.first_name} {policy.customer_inn}',
            str(policy.sale_date),
            str(policy.profit_summ),
            str(policy.commission_summ),
        ])
        inc += 1
        total_profit += policy.profit_summ
        total_commission += policy.commission_summ
    data.append([
        "",
        "Итого",
        "",
        str(total_profit),
        str(total_commission)
        ]
    )

    tableStyle = [
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]

    styleN = styles['Normal']
    styleN.wordWrap = 'CJK'

    styleN.fontName = 'TimesNewRoman'  # Установка загруженного шрифта

    data2 = [[Paragraph(cell, styleN) for cell in row] for row in data]

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')

    colwidths = [frame._width * 0.1]  # Устанавливаем ширину для первого столбца
    colwidths.extend([frame._width * 0.21 for _ in range(4)])

    t = LongTable(data2, colWidths=colwidths)
    t.setStyle(TableStyle(tableStyle))
    elements.append(t)

    template = PageTemplate(id='longtable', frames=frame)
    doc.addPageTemplates([template])
    doc.build(elements)
    return filename
