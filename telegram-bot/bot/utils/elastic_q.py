from typing import List
from typing import Union
from datetime import datetime as dt

def filter_q(*filters: dict) -> List[dict]:
    filters_q = [f for f in filters if len(f) > 0]
    return {'filter': filters_q}

def range_q(gte: Union[dt, None], lte: Union[dt, None]) -> dict:
    if gte is None and lte is None: return {}

    q = {'range': {'date': {'format': 'epoch_second'}}}
    if gte is not None: q['range']['date']['gte'] = int(gte.timestamp())
    if lte is not None: q['range']['date']['lte'] = int(lte.timestamp())
    return q
