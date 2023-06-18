from typing import Union
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
from datetime import datetime as dt

from ndt.es7.utils import es_keyword, es_float, es_date_s

import dataclasses_json
dataclasses_json.global_config.encoders[dt] = lambda dt: int(dt.timestamp())
dataclasses_json.global_config.decoders[dt] = lambda ts: dt.fromtimestamp(ts)


@dataclass
class Item(DataClassJsonMixin):
	name: str
	cost: float
	date: dt
	category: Union[str, None] = None
	establishment: Union[str, None] = None
	timestamp: dt = field(metadata=config(field_name='@timestamp'), default=dt.now())

	@staticmethod
	def mapping(): return {
		'name': es_keyword,
		'cost': es_float,
		'date': es_date_s,
		'category': es_keyword,
		'establishment': es_keyword,
		'@timestamp': es_date_s
	}

	@staticmethod
	def datefield(): return 'date'

	def str_for_list(self) -> str:
		opt_fields = [v for v in {self.category, self.establishment} if v is not None]
		template_fields = {
			'date': self.date.strftime('%Y-%m-%d'),
			'name': self.name,
			'cost': self.cost,
			'opt' : ', '.join(opt_fields)
		} 

		if len(opt_fields) == 0: return '{date}: {name} - {cost}€'.format(**template_fields)
		return '{date}: {name} - {cost}€ ({opt})'.format(**template_fields)
