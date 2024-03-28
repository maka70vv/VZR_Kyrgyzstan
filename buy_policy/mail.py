from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_notification_on_save(travel_agency, mail_users):
    send_mail(
        f'Создан новый страховой полис - {travel_agency}',
        'Посмотреть в CRM: ',
        'noreply@insurance.kg',
        mail_users,
    )


def send_notification_on_delete():
    send_mail(
        'Subject: Тестовое письмо',
        'This is a test message.',
        'noreply@insurance.kg',
        ['it@insurance.kg'],
    )


def send_notification_to_user_on_save(user_email, price_kgs):
    signature = render_to_string('signature.html')
    message = (f'Уважаемый клиент! Вами был приобретен страховой полис по программе Выезд за рубеж на сумму {price_kgs} сом!'
               f'{signature}')

    send_mail(
        f'Страховой полис успешно зарегистрирован!',
        message,
        'noreply@insurance.kg',
        [user_email, ],
        html_message=message
    )
