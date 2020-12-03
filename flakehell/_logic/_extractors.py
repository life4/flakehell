# built-in
import ast
import re
from importlib import import_module
from pathlib import Path
from typing import Dict, List


REX_CODE = re.compile(r'^[A-Z]{1,5}[0-9]{1,5}$')
ALIASES = {
    'flake8_bugbear': 'bugbear',
    'flake8_logging_format': 'logging_format',
}


class CollectStrings(ast.NodeVisitor):
    _strings: List[str]

    def visit_Str(self, node):
        self._strings.append(node.s)


def get_messages(code: str, content: str) -> Dict[str, str]:
    root = ast.parse(content)
    CollectStrings._strings = []
    collector = CollectStrings()
    collector.visit(root)

    messages = dict()
    for message in collector._strings:
        message_code, _, message_text = message.partition(' ')
        if not message_text:
            continue
        message_code = message_code.rstrip(':')
        if not REX_CODE.match(message_code):
            continue
        if code and not message_code.startswith(code):
            continue
        messages[message_code] = message_text
    return messages


def extract_default(name: str) -> Dict[str, str]:
    module = import_module(name)
    content = Path(module.__file__).read_text()
    return get_messages(code='', content=content)


def extract(name) -> Dict[str, str]:
    name = name.replace('-', '_')
    name = ALIASES.get(name, name)
    function_name = 'extract_' + name

    # use ad-hoc extractor if available
    if function_name in globals():
        return globals()[function_name]()

    # try to extract by default algorithm
    return extract_default(name)


# -- EXTRACTORS WITH A CUSTOM PATH -- #


def extract_flake8_absolute_import() -> Dict[str, str]:
    return extract_default(name='flake8_absolute_import.core')


def extract_flake8_aaa() -> Dict[str, str]:
    return extract_default(name='flake8_aaa.line_markers')


def extract_flake8_cognitive_complexity() -> Dict[str, str]:
    return extract_default(name='flake8_cognitive_complexity.checker')


def extract_flake8_variables_names() -> Dict[str, str]:
    return extract_default(name='flake8_variables_names.checker')


def extract_logging_format() -> Dict[str, str]:
    return extract_default(name='logging_format.violations')


def extract_flake8_sql() -> Dict[str, str]:
    return extract_default(name='flake8_sql.linter')


def extract_flake8_requirements() -> Dict[str, str]:
    return extract_default(name='flake8_requirements.checker')


def extract_flake8_expression_complexity() -> Dict[str, str]:
    return extract_default(name='flake8_expression_complexity.checker')


def extract_flake8_use_fstring() -> Dict[str, str]:
    codes = dict()
    codes.update(extract_default(name='flake8_use_fstring.format'))
    codes.update(extract_default(name='flake8_use_fstring.percent'))
    # https://github.com/MichaelKim0407/flake8-use-fstring/pull/2
    try:
        codes.update(extract_default(name='flake8_use_fstring.prefix'))
    except ImportError:
        pass
    return codes


def extract_flake8_functions() -> Dict[str, str]:
    codes = dict()
    codes.update(extract_default('flake8_functions.checker'))
    try:
        codes.update(extract_default('flake8_functions.function_arguments_amount'))
        codes.update(extract_default('flake8_functions.function_lenght'))
        codes.update(extract_default('flake8_functions.function_purity'))
    except ImportError:
        pass
    return codes


# -- HARDCODED CODES -- #


def extract_flake8_spellcheck() -> Dict[str, str]:
    return {
        'SC100': 'Spelling error in comments',
        'SC200': 'Spelling error in name',
    }


def extract_flake8_import_order() -> Dict[str, str]:
    return {
        'I666': 'Import statement mixes groups.',
        'I100': 'Import statements are in the wrong order.',
        'I101': 'Imported names are in the wrong order.',
        'I201': 'Missing newline between import groups.',
        'I202': 'Additional newline in a group of imports.',
    }


def extract_flake8_black() -> Dict[str, str]:
    from flake8_black import black_prefix

    return {
        black_prefix + '901': 'Invalid input',
        black_prefix + '997': 'Invalid TOML file',
        black_prefix + '999': 'Unexpected exception',
    }


def extract_flake8_alfred() -> Dict[str, str]:
    return {'B1': 'banned symbol'}


def extract_flake8_eradicate() -> Dict[str, str]:
    return {'E800': 'Found commented out code: {0}'}


# -- AD-HOC EXTRACTORS -- #


def extract_flake8_commas() -> Dict[str, str]:
    from flake8_commas._base import ERRORS

    return dict(ERRORS.values())


def extract_flake8_debugger() -> Dict[str, str]:
    from flake8_debugger import DEBUGGER_ERROR_CODE
    return {DEBUGGER_ERROR_CODE: 'trace found'}


def extract_flake8_mutable() -> Dict[str, str]:
    from mutable_defaults import MutableDefaultChecker

    return {MutableDefaultChecker._code: MutableDefaultChecker._error_tmpl}


def extract_flake8_fixme() -> Dict[str, str]:
    from flake8_fixme import WORD_CODES

    return {code: 'fixme found ({})'.format(word) for word, code in WORD_CODES.items()}


def extract_pep8_naming() -> Dict[str, str]:
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


def extract_flake8_pyi() -> Dict[str, str]:
    import pyi
    codes = dict()
    for name, value in vars(pyi).items():
        if name.startswith('Y0'):
            codes[name] = value
    return codes


def extract_flake8_pytest_style() -> Dict[str, str]:
    from flake8_pytest_style import errors
    codes = dict()
    for error in vars(errors).values():
        if error is errors.Error:
            continue
        if not isinstance(error, type):
            continue
        if not issubclass(error, errors.Error):
            continue
        codes[error.code] = error.message  # type: ignore
    return codes


def extract_flake8_annotations_complexity() -> Dict[str, str]:
    from flake8_annotations_complexity.checker import AnnotationsComplexityChecker

    code, message = AnnotationsComplexityChecker._error_message_template.split(' ', maxsplit=1)
    return {code: message}


def extract_flake8_future_import() -> Dict[str, str]:
    from flake8_future_import import ALL_FEATURES
    codes = dict()
    tmpl = 'FI{}'
    for feature in ALL_FEATURES:
        code = tmpl.format(10 + feature.index)
        codes[code] = '__future__ import "{}" missing'.format(feature.name)
        code = tmpl.format(50 + feature.index)
        codes[code] = '__future__ import "{}" present'.format(feature.name)
    codes[tmpl.format(90)] = '__future__ import does not exist'
    return codes


def extract_flake8_string_format() -> Dict[str, str]:
    from flake8_string_format import StringFormatChecker

    return {'P{}'.format(c): m for c, m in StringFormatChecker.ERRORS.items()}


def extract_flake8_bandit() -> Dict[str, str]:
    from bandit.core.extension_loader import MANAGER

    codes = dict()
    for blacklist in MANAGER.blacklist.values():
        for check in blacklist:
            code = check['id'].replace('B', 'S')
            codes[code] = check['message']
    for plugin in MANAGER.plugins:
        code = plugin.plugin._test_id.replace('B', 'S')
        codes[code] = plugin.name.replace('_', ' ')
    return codes


def extract_pylint() -> Dict[str, str]:
    import pylint.checkers
    try:
        from pylint.lint import MSGS
    except ImportError:
        from pylint.lint.pylinter import MSGS

    codes = dict()
    for code, (msg, alias, *_) in MSGS.items():
        if msg in ('%s', '%s: %s'):
            msg = alias.replace('-', ' ')
        codes[code] = msg.replace('\n', ' ')

    for path in Path(pylint.checkers.__path__[0]).iterdir():
        module = import_module('pylint.checkers.' + path.stem)
        for class_name in dir(module):
            cls = getattr(module, class_name, None)
            msgs = getattr(cls, 'msgs', None)
            if not msgs:
                continue
            for code, (msg, alias, *_) in msgs.items():
                if msg in ('%s', '%s: %s'):
                    msg = alias.replace('-', ' ')
                codes[code] = msg.replace('\n', ' ')
    return codes


def extract_pyflakes() -> Dict[str, str]:
    from flake8.plugins.pyflakes import FLAKE8_PYFLAKES_CODES
    from pyflakes import messages

    codes = dict()
    for class_name, code in FLAKE8_PYFLAKES_CODES.items():
        codes[code] = getattr(messages, class_name).message
    return codes


def extract_flake8_rst_docstrings() -> Dict[str, str]:
    from flake8_rst_docstrings import code_mappings_by_level

    codes = dict()
    for level, codes_mapping in code_mappings_by_level.items():
        for message, number in codes_mapping.items():
            code = 'RST{}{:02d}'.format(level, number)
            codes[code] = message
    return codes


def extract_flake8_django() -> Dict[str, str]:
    import flake8_django.checkers

    codes = dict()
    for path in Path(flake8_django.checkers.__path__[0]).iterdir():
        module = import_module('flake8_django.checkers.' + path.stem)
        for class_name in dir(module):
            cls = getattr(module, class_name, None)
            if not hasattr(cls, 'code'):
                continue
            if '0' not in cls.__name__:
                continue
            codes[cls.__name__] = cls.description
    return codes


def extract_flake8_scrapy() -> Dict[str, str]:
    from flake8_scrapy import ScrapyStyleIssueFinder

    codes = dict()
    for finders in ScrapyStyleIssueFinder().finders.values():
        for finder in finders:
            codes[finder.msg_code] = finder.msg_info
    return codes


def extract_flake8_executable() -> Dict[str, str]:
    import flake8_executable

    path = Path(flake8_executable.__file__)
    content = path.read_text()
    codes = dict()
    for code, msg in re.findall(r"'(EXE00\d)', '(.*)'", content):
        codes[code] = msg
    return codes


def extract_flake8_strict() -> Dict[str, str]:
    from flake8_strict import ErrorCode

    codes = dict()
    for code, message in ErrorCode._member_map_.items():
        codes[code] = message.value
    return codes


def extract_flake8_docstrings() -> Dict[str, str]:
    from pydocstyle.violations import ErrorRegistry

    codes = dict()
    for group in ErrorRegistry.groups:
        for error in group.errors:
            codes[error.code] = error.short_desc
    return codes


def extract_dlint() -> Dict[str, str]:
    from dlint.linters import ALL

    codes = dict()
    for linter in ALL:
        code, msg = linter._error_tmpl.split(' ', maxsplit=1)
        codes[code] = msg
    return codes


def extract_flake8_mock() -> Dict[str, str]:
    from flake8_mock import MOCK_ERROR_CODE, ERROR_MESSAGE

    message = ERROR_MESSAGE.split(' ', maxsplit=1)[1]
    return {MOCK_ERROR_CODE: message}


def extract_flake8_pytest() -> Dict[str, str]:
    from flake8_pytest import PYTEST_ERROR_CODE, PYTEST_ERROR_MESSAGE

    return {PYTEST_ERROR_CODE: PYTEST_ERROR_MESSAGE}


def extract_wemake_python_styleguide() -> Dict[str, str]:
    from wemake_python_styleguide import violations

    codes = dict()
    for path in Path(violations.__path__[0]).iterdir():
        module = import_module('wemake_python_styleguide.violations.' + path.stem)
        for checker_name in dir(module):
            if not checker_name.endswith('Violation'):
                continue
            checker = getattr(module, checker_name)
            if not hasattr(checker, 'code'):
                continue
            code = 'WPS' + str(checker.code).zfill(3)
            codes[code] = checker.error_template
    return codes
