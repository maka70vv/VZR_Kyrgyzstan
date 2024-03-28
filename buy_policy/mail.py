from django.core.mail import send_mail


def send_notification_on_save(travel_agency):
    send_mail(
        f'Создан новый страховой полис - {travel_agency}',
        'Посмотреть в CRM: ',
        'noreply@insurance.kg',
        ['it@insurance.kg'],
    )


def send_notification_on_delete():
    send_mail(
        'Subject: Тестовое письмо',
        'This is a test message.',
        'noreply@insurance.kg',
        ['it@insurance.kg'],
    )
