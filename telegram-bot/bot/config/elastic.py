import os
from datetime import datetime as dt

host = os.getenv('ES_HOST', 'localhost')
items_index = 'items'