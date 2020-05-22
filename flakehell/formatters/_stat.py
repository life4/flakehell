# built-in
from collections import defaultdict
from typing import DefaultDict, Dict

# external
from flake8.style_guide import Violation
from termcolor import colored

# app
from .._logic import color_code, color_description
from ._colored import ColoredFormatter


class StatFormatter(ColoredFormatter):
    """
    Show count of every code occurance
    """
    _codes: DefaultDict[str, DefaultDict[str, int]]
    _msgs: DefaultDict[str, Dict[str, str]]

    def after_init(self) -> None:
        super().after_init()
        self._codes = defaultdict(lambda: defaultdict(int))
        self._msgs = defaultdict(dict)

    def format(self, error: Violation) -> None:
        plugin = getattr(error, 'plugin', '')
        self._codes[plugin][error.code] += 1
        self._msgs[plugin][error.code] = error.text

    def stop(self) -> None:
        for plugin, codes in sorted(self._codes.items()):
            self._write(colored(plugin, 'green'))
            for code, count in sorted(codes.items(), key=lambda x: x[-1], reverse=True):
                self._write('  {code:} | {count:>5} | {msg}'.format(
                    code=color_code(code.ljust(6)),
                    count=count,
                    msg=color_description(self._msgs[plugin][code]),
                ))
