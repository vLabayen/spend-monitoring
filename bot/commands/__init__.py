from typing import Callable
from dataclasses import dataclass
from argparse import ArgumentParser

@dataclass
class Command:
	name: str
	help: str
	configure_parser: Callable[[ArgumentParser], None]
	handler: callable