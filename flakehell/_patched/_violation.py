# built-in
from collections import namedtuple

# external
from flake8.style_guide import Violation


# the same as in flake8, but with some additional fields
_Violation = namedtuple(
    'Violation',
    [
        'code',
        'filename',
        'line_number',
        'column_number',
        'text',
        'physical_line',

        # added fields
        'plugin',
    ],
)


class FlakeHellViolation(_Violation):
    """Patched flake8.style_guide.Violation

    We can't just inherit because Violation is a namedtuple,
    and we can't add new fields.
    """

    def is_inline_ignored(self, disable_noqa):
        return Violation.is_inline_ignored(self, disable_noqa)

    def is_in(self, diff):
        return Violation.is_in(self, diff)
