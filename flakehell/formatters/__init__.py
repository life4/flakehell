from ._baseline import BaseLineFormatter
from ._colored import ColoredFormatter
from ._grouped import GroupedFormatter
from ._json import JSONFormatter
from ._stat import StatFormatter


FORMATTERS = dict(
    baseline=BaseLineFormatter,
    colored=ColoredFormatter,
    grouped=GroupedFormatter,
    json=JSONFormatter,
    stat=StatFormatter,
)
