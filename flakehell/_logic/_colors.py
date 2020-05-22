# built-in
import re

# external
from termcolor import colored


COLORS = dict(
    W='yellow',
    E='red',
    F='red',
    WPS='magenta',
)
REX_CODE = re.compile(r'([A-Z]+)([0-9]+)')
REX_TEXT = re.compile('[A-Z]+')
REX_NUMBER = re.compile('( [0-9]+)')
REX_PLACEHOLDER = re.compile(r'(\{[a-z0-9]+\}|\%[a-z])')
REX_QUOTES = re.compile(
    r"""
        (   # quotted text
            [\"\'\`]
            [\w\_\-\.\%\+\*]
            [\w\_\-\.\%\+\*\s\:]*
            [\"\'\`]
        )
        | (__[a-z]+__)                      # magic method
        | ([a-z\_]+\.py)                    # file name
        | (\:\s)([\w0-9]+$)                 # word after :
        | ([A-Z][a-z\.]+(?:[A-Z][a-z\.]+)+) # CamelCase
        | ([a-z_]+\(\))                     # function
    """,
    re.X,
)


def color_code(code: str) -> str:
    match = REX_TEXT.match(code)
    color = 'blue'
    if match:
        color = COLORS.get(match.group(), color)
    return REX_CODE.sub(colored(r'\1', color) + colored(r'\2', 'cyan'), code)


def color_description(text: str) -> str:
    text = REX_NUMBER.sub(colored(r'\1', 'green'), text)
    text = REX_QUOTES.sub(r'\4' + colored(r'\1\2\3\5\6\7', 'yellow'), text)
    text = REX_PLACEHOLDER.sub(colored(r'\1', 'green'), text)
    return text
