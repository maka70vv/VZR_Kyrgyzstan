import os
from datetime import timedelta, datetime

from celery import shared_task
from django.core.files.base import ContentFile

from buy_policy.models import BuyPolicy
from mail_users.mail import send_reports
from mail_users.models import MailUser
from reports.models import Report, Invoice
from reports.reports_pdf import pdf_generator_reports, pdf_generator_invoices
from travel_agency.models import TravelAgency


@shared_task
def generate_report():
    today = datetime.now().date()
    last_month = today.replace(day=1) - timedelta(days=1)
    start_date = last_month.replace(day=27)
    mail_users = MailUser.objects.all()

    report_urls = []
    invoices = []

    for travel_agency in TravelAgency.objects.all():
        policies = BuyPolicy.objects.filter(travel_agency=travel_agency, sale_date__gte=start_date)
        report_file = pdf_generator_reports(policies, travel_agency, start_date)
        invoice_file = pdf_generator_invoices(policies, travel_agency, start_date)

        report = Report.objects.create(
            travel_agency=travel_agency,
        )

        invoice = Invoice.objects.create(
            travel_agency=travel_agency,
        )

        with open(report_file, 'rb') as f:
            report.file.save(report_file, ContentFile(f.read()), save=True)

        with open(invoice_file, 'rb') as f:
            invoice.file.save(invoice_file, ContentFile(f.read()), save=True)

        os.remove(report_file)
        os.remove(invoice_file)

        report_urls.append(f'localhost:8000{report.file.url}')

        invoices.append(f'localhost:8000{invoice.file.url}')

    send_reports(today, report_urls, mail_users, invoices)
