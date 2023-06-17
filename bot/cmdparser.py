import argparse
import logging
import shlex

class ParserHelp(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class ParserError(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class CmdParser(argparse.ArgumentParser):
    ignore_args = {'command', 'handler', 'parser', 'help'}

    def error(self, message: str, *args, **kwargs):
        raise ParserError(messages = [message, self.format_help()])

    def print_help(self, *args, **kwargs) -> None:
        raise ParserHelp(message = self.format_help())

    def parse_args(self, cmd: str) -> argparse.Namespace:
        return super().parse_args(shlex.split(cmd))

    @staticmethod
    def get_kwargs(args: argparse.Namespace) -> dict:
        return {name: value for name, value in vars(args).items() if name not in CmdParser.ignore_args}

