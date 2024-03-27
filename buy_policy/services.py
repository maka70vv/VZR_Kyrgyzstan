from datetime import date


def calculate_age(birth_date: date) -> int:
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def calculate_coefficient(age: int, skiing: bool, sport_activities: bool, dangerous_activities: bool,
                          insured: int) -> float:
    if 60 <= age < 65 or 2 <= age < 3:
        coefficient = 2
    elif 65 <= age < 70:
        coefficient = 3
    elif age >= 70 or age < 2:
        raise ValueError("Невозможно застраховать клиента, так как возраст >= 70 лет или меньше 2 лет")
    elif 3 <= age < 14:
        coefficient = 0.85
    else:
        coefficient = 1

    if skiing:
        coefficient *= 2
    if sport_activities or dangerous_activities:
        coefficient *= 2.5
    if insured >= 7:
        coefficient *= 0.90

    return coefficient


def calculate_price(validity_period: int, coefficient: float, insurance_summ) -> float:
    if 1 <= validity_period <= 7:
        return insurance_summ.price_up_to_7days * coefficient * validity_period
    elif 8 <= validity_period <= 15:
        return insurance_summ.price_up_to_15days * coefficient * validity_period
    elif 16 <= validity_period <= 30:
        return insurance_summ.price_up_to_30days * coefficient * validity_period
    elif 31 <= validity_period <= 90:
        return insurance_summ.price_up_to_90days * coefficient * validity_period
    elif 91 <= validity_period <= 180:
        return insurance_summ.price_up_to_180days * coefficient * validity_period
    elif 181 <= validity_period <= 365:
        return insurance_summ.price_up_to_365days * coefficient * validity_period


def convert_to_kgs(price: float, insurance_summ, exchange_rates) -> float:
    if insurance_summ.currency == 'EUR':
        eur_rate = float(exchange_rates.eur_rate)
        price_kgs = round(price * eur_rate, 2)
    elif insurance_summ.currency == 'USD':
        usd_rate = float(exchange_rates.usd_rate)
        price_kgs = round(price * usd_rate, 2)
    elif insurance_summ.currency == 'RUB':
        rub_rate = float(exchange_rates.rub_rate)
        price_kgs = round(price * rub_rate, 2)
    else:
        price_kgs = round(price, 2)
    return price_kgs


def calculate_taxes(price: float):
    return round(price * 0.3, 2)


def calculate_price_with_taxes(price: float, taxes: float) -> float:
    price_with_taxes = price + taxes
    return round(price_with_taxes, 2)


def calculate_commission_summ(price: float, commission: int) -> float:
    commission_summ = round(price * (commission / 2), 2)
    return commission_summ


def calculate_profit(price: float, commission_summ: float) -> float:
    profit_summ = price - commission_summ
    return profit_summ


def save_insurance_price(birth_date: date, skiing: bool, sport_activities: bool, dangerous_activities: bool,
                         start_date: date, end_date: date, insurance_summ, exchange_rates, insured, commission) -> float:
    age = calculate_age(birth_date)
    coefficient = calculate_coefficient(age, skiing, sport_activities, dangerous_activities, insured)
    validity_period = (end_date - start_date).days
    price = calculate_price(validity_period, coefficient, insurance_summ)
    price_kgs = convert_to_kgs(price, insurance_summ, exchange_rates)
    taxes_summ = calculate_taxes(price_kgs)
    taxes_summ_exchange = calculate_taxes(price)
    price_with_taxes = calculate_price_with_taxes(price_kgs, taxes_summ)
    price_exchange = calculate_price_with_taxes(price, taxes_summ_exchange)
    commission_summ = calculate_commission_summ(price_kgs, commission)
    profit = calculate_profit(price_kgs, commission_summ)
    prices = {
        "age": age,
        "price_exchange": price_exchange,
        "price_kgs": price_with_taxes,
        "taxes_summ": taxes_summ,
        "price_without_taxes": price_kgs,
        "commission_summ": commission_summ,
        "profit": profit
    }
    return prices


def calculate_insurance_price(birth_date: date, skiing: bool, sport_activities: bool, dangerous_activities: bool,
                              start_date: date, end_date: date, insurance_summ, exchange_rates, insured) -> float:
    age = calculate_age(birth_date)
    coefficient = calculate_coefficient(age, skiing, sport_activities, dangerous_activities, insured)
    validity_period = (end_date - start_date).days
    price = calculate_price(validity_period, coefficient, insurance_summ)
    price_kgs = convert_to_kgs(price, insurance_summ, exchange_rates)
    taxes_summ = calculate_taxes(price_kgs)
    taxes_summ_exchange = calculate_taxes(price)
    price_with_taxes = calculate_price_with_taxes(price_kgs, taxes_summ)
    price_exchange = calculate_price_with_taxes(price, taxes_summ_exchange)
    prices = {
        "price_exchange": price_exchange,
        "price_kgs": price_with_taxes
    }
    return prices
