import requests


def send_policy(policy, **kwargs):
    data = {
        "customer_individual": {
            "passport": {
                "inn": policy.customer_inn,
                "series_number": policy.passport_series_num,
                "sex": policy.sex,
                "birth_date": policy.birth_date,
            },
            "last_name": policy.last_name,
            "first_name": policy.first_name,
        },
        "policy_number": f'ВЗР-{policy.policy_id}',
        "status": "На рассмотрении",
        "start_date": policy.start_date,
        "end_date": policy.end_date,
        "currency_letter_code": policy.insurance_summ.currency,
        "sum_insured": policy.insurance_summ.insurance_summ,
        "insurance_premium": policy.price_with_taxes_kgs,
        "territory": policy.insurance_summ.country.name,
        "purpose": policy.purpose,
        "payment": 2
    }

    if policy.phone_number is not None:
        data["phone_numbers"] = [{"phone_number": policy.phone_number, "phone_type": policy.phone_type}]

    if policy.email is not None:
        data["emails"] = {"email": policy.email}

    if policy.patronymic is not None:
        data['customer_individual']["patronymic"] = policy.patronymic
    if policy.risks:
        risk_ids = [risk.crm_id for risk in policy.risks.all()]
        data["additional_info"] = risk_ids

    url = "http://192.168.0.38/api_business/travel/"
    # response = requests.post(url, json=data)

    return data

