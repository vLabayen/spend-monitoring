from typing import Callable
from types import ModuleType
from dataclasses import dataclass
from argparse import ArgumentParser

@dataclass
class Command:
	name: str
	help: str
	configure_parser: Callable[[ArgumentParser], None]
	handler: callable
	init: Callable[[], bool] = lambda: True

	@staticmethod
	def from_module(name: str, module: ModuleType) -> 'Command':
		return Command(name,
			help = module.help,
			configure_parser = module.configure_parser,
			handler = module.handler,
			init = getattr(module, 'init', lambda: True),
		)

	def __repr__(self) -> str:
		return f'Command({self.name!r}, help={self.help!r})'
