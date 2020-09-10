# built-in
from typing import Tuple, Union

# app
from ._constants import ExitCode


CommandResult = Tuple[Union[int, ExitCode], str]
