"""Flake8 wrapper to make it nice and configurable
"""

# app
from ._cli import entrypoint, flake8_entrypoint
from ._version import __version__


__all__ = ['entrypoint', 'flake8_entrypoint', '__version__']
