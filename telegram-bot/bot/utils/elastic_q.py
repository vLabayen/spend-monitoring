from typing import Union
from datetime import datetime as dt

def range_q(gte: Union[dt, None], lte: Union[dt, None]) -> dict:
    if gte is None and lte is None: return {}

    q = {'range': {'date': {'format': 'epoch_second'}}}
    if gte is not None: q['range']['date']['gte'] = int(gte.timestamp())
    if lte is not None: q['range']['date']['lte'] = int(lte.timestamp())
    return q
