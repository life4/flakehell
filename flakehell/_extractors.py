import ast
import re
from pathlib import Path


REX_CODE = re.compile(r'^[A-Z]{1,5}[0-9]{1,5}$')


class CollectStrings(ast.NodeVisitor):
    _strings = []

    def visit_Str(self, node):
        self._strings.append(node.s)


def get_messages(code, content):
    root = ast.parse(content)
    collector = CollectStrings()
    collector.visit(root)

    messages = dict()
    for message in collector._strings:
        message_code, _, message_text = message.partition(' ')
        if not message_text:
            continue
        if not REX_CODE.match(message_code):
            continue
        if code and not message_code.startswith(code):
            continue
        messages[message_code] = message_text
    return messages


def extract_default(name):
    module = __import__(name)
    content = Path(module.__file__).read_text()
    return get_messages(code='', content=content)


def extract(name):
    function_name = 'extract_' + name.replace('-', '_')

    # use ad-hoc extractor if available
    if function_name in globals():
        return globals()[function_name]()

    # try to extract by default algorithm
    return extract_default(name)


# AD-HOC EXTRACTORS


def extract_flake8_commas():
    from flake8_commas._base import ERRORS

    return dict(ERRORS.values())


def extract_flake8_quotes():
    import flake8_quotes

    content = Path(flake8_quotes.__file__).read_text()
    return get_messages(code='Q0', content=content)


def extract_flake8_variables_names():
    from flake8_variables_names import checker

    content = Path(checker.__file__).read_text()
    return get_messages(code='VNE', content=content)


def extract_logging_format():
    from logging_format import violations

    content = Path(violations.__file__).read_text()
    return get_messages(code='G', content=content)


def extract_flake8_debugger():
    from flake8_debugger import DEBUGGER_ERROR_CODE
    return {DEBUGGER_ERROR_CODE: 'trace found'}


def extract_flake_mutable():
    from mutable_defaults import MutableDefaultChecker

    return {MutableDefaultChecker._code: MutableDefaultChecker._error_tmpl}


def extract_pep8ext_naming():
    import pep8ext_naming

    codes = dict()
    for checker_name in dir(pep8ext_naming):
        if not checker_name.endswith('Check'):
            continue
        checker = getattr(pep8ext_naming, checker_name)
        for code, message in checker.__dict__.items():
            if code[0] == 'N':
                codes[code] = message
    return codes
