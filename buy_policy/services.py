from datetime import date


def calculate_age(birth_date: date) -> int:
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def calculate_coefficient(age: int, skiing: bool, sport_activities: bool, dangerous_activities: bool) -> float:
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


def calculate_insurance_price(birth_date: date, skiing: bool, sport_activities: bool, dangerous_activities: bool,
                              start_date: date, end_date: date, insurance_summ) -> float:
    age = calculate_age(birth_date)
    coefficient = calculate_coefficient(age, skiing, sport_activities, dangerous_activities)
    validity_period = (end_date - start_date).days
    price = calculate_price(validity_period, coefficient, insurance_summ)
    return price
              