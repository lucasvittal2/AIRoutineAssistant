from datetime import timedelta, datetime
import pytz

def string_to_timedelta(str_freq: str, sep: str= ':'):
    days, hours, minutes, seconds = map(float, str_freq.split(sep))
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

def string_to_datetime(str_datetime: str, str_format: str = '%Y-%m-%d', timezone: str = 'America/Sao_Paulo'):
    return pytz.timezone(timezone).localize(datetime.strptime(str_datetime, str_format))