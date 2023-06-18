import re
from ndt.time_handler import rtime2datetime
from datetime import datetime as dt

date_rgx = re.compile(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}')
def date(date: str) -> dt:
    if date_rgx.match(date): return dt.strptime(date, '%Y-%m-%d-%H-%M-%S')
    return rtime2datetime(date)
