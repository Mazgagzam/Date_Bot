from datetime import datetime
from dateutil.relativedelta import relativedelta


async def get_distance(date1: datetime, date2: datetime):
    date = relativedelta(date1, date2)

    return date