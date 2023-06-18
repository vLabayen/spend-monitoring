import os
from datetime import datetime as dt

host = os.getenv('ES_HOST', 'localhost')

items_index_pattern = 'items*'
items_index = lambda: f'items+{dt.now().year}'