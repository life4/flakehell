# built-in
from typing import Tuple, Union
from ._constants import ExitCodes


CommandResult = Tuple[Union[int, ExitCodes], str]
