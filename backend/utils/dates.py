from datetime import datetime, timedelta


def parse_date(value: str, label: str = "date") -> datetime:
    if not value:
        raise ValueError(f"{label} is required")

    text = str(value).strip()[:10]
    try:
        return datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid {label}. Use YYYY-MM-DD")


def date_str(value) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    text = str(value)
    return text[:10]


def nights_between(start: str, end: str) -> int:
    start_date = parse_date(start, "travel_start_date")
    end_date = parse_date(end, "travel_end_date")
    nights = (end_date - start_date).days
    if nights < 1:
        raise ValueError("travel_end_date must be after travel_start_date")
    return nights


def add_days(start: str, days: int) -> str:
    return (parse_date(start) + timedelta(days=max(days, 1))).strftime("%Y-%m-%d")


def ranges_overlap(start_a: str, end_a: str, start_b: str, end_b: str) -> bool:
    a1 = parse_date(start_a)
    a2 = parse_date(end_a)
    b1 = parse_date(start_b)
    b2 = parse_date(end_b)
    return a1 < b2 and b1 < a2
