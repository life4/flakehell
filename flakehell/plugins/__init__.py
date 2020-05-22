
# app
from ._pylint import PyLintChecker


# try:
#     from ._pylint import PyLintChecker
# except ImportError:
#     PyLintChecker = None


PLUGINS = dict(
    pylint=PyLintChecker,
)

__all__ = [
    'PLUGINS',
    'PyLintChecker',
]
