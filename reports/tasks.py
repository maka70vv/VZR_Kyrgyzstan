from datetime import timedelta, datetime

from celery import shared_task

from buy_policy.models import BuyPolicy
from reports.models import Report
from reports.reports_pdf import pdf_generator_reports
from travel_agency.models import TravelAgency


@shared_task
def generate_report():
    today = datetime.now().date()
    last_month = today.replace(day=1) - timedelta(days=1)
    start_date = last_month.replace(day=27)

    for travel_agency in TravelAgency.objects.all():
        policies = BuyPolicy.objects.filter(travel_agency=travel_agency, sale_date__gte=start_date)
        file = pdf_generator_reports(policies, travel_agency, start_date)

        report = Report.objects.create(
            travel_agency=travel_agency,
        )

        with open(file, 'rb') as f:
            from django.core.files.base import ContentFile
            report.file.save(file, ContentFile(f.read()), save=True)


