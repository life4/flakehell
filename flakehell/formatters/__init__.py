from ._colored import ColoredFormatter
from ._grouped import GroupedFormatter
from ._json import JSONFormatter


FORMATTERS = dict(
    colored=ColoredFormatter,
    grouped=GroupedFormatter,
    json=JSONFormatter,
)
