from datetime import datetime, timedelta
from typing import List

from tmt.clocking.models import Clock


def get_first_week_day(today) -> datetime:
    # assume that start from monday
    day_num = timedelta(days=today.weekday())
    return today - day_num


def get_clocked_hours(clocks: List[Clock]) -> int:
    timedelta_list = [(clock.clocked_out - clock.clocked_in) for clock in clocks]
    total_seconds = sum(timedelta_list, timedelta()).total_seconds()
    total_hours = round(total_seconds / 3600.)
    return int(total_hours)
