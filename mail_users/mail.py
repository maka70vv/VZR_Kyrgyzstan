from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_notification_on_save(travel_agency, mail_users):
    signature = render_to_string('signature.html')
    message = (f'Посмотреть в CRM: '
               f'{signature}')
    send_mail(
        f'Создан новый страховой полис - {travel_agency}',
        message,
        'noreply@insurance.kg',
        mail_users,
        html_message=message
    )


def send_notification_on_delete():
    signature = render_to_string('signature.html')
    send_mail(
        'Subject: Тестовое письмо',
        'This is a test message.',
        'noreply@insurance.kg',
        ['it@insurance.kg'],

    )


def send_notification_to_user_on_save(user_email, price_kgs):
    signature = render_to_string('signature.html')
    message = (
        f'Уважаемый клиент! Вами был приобретен страховой полис по программе Выезд за рубеж на сумму {price_kgs} сом!'
        f'{signature}')

    send_mail(
        f'Страховой полис успешно зарегистрирован!',
        message,
        'noreply@insurance.kg',
        [user_email, ],
        html_message=message
    )


def send_reports(today, reports, mail_users, invoices):
    links_html = ''
    links_invoices_html = ''
    for report_link in reports:
        links_html += f'<a href="{report_link}">{report_link}</a><br>'
    for invoice_link in invoices:
        links_invoices_html += f'<a href="{invoice_link}">{invoice_link}</a><br>'

    signature = render_to_string('signature.html')

    message = f'Отчеты от тур. компаний за {today}<br>{links_html}<br>Счета на оплату<br>{links_invoices_html}{signature}'

    # Отправка электронной почты
    send_mail(
        f'Отчеты ВЗР за {today}',
        message,
        'noreply@insurance.kg',
        mail_users,
        html_message=message
    )
