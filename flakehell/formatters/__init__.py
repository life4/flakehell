from ._colored import ColoredFormatter
from ._json import JSONFormatter

FORMATTERS = dict(
    colored=ColoredFormatter,
    json=JSONFormatter,
)
