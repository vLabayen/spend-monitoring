import argparse
import logging
import shlex

class ParserHelp(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class ParserError(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class HelpAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser: argparse.ArgumentParser, *args, **kwargs):
        print(parser, args, kwargs)
        raise ParserHelp(message = parser.format_help())

class CmdParser(argparse.ArgumentParser):
    ignore_args = {'command', 'handler', 'parser', 'help'}

    def error(self, message: str, *args, **kwargs):
        raise ParserError(messages = [message, self.format_help()])

    def parse_args(self, cmd: str) -> argparse.Namespace:
        return super().parse_args(shlex.split(cmd))

    @staticmethod
    def get_kwargs(args: argparse.Namespace) -> dict:
        return {name: value for name, value in vars(args).items() if name not in CmdParser.ignore_args}

