# built-in
from functools import lru_cache

# external
from flake8.style_guide import StyleGuide, StyleGuideManager

# app
from ._violation import FlakeHellViolation


class FlakeHellStyleGuideManager(StyleGuideManager):
    def __init__(self, options, formatter, decider=None):
        """Initialize our StyleGuide.

        .. todo:: Add parameter documentation.
        """
        super().__init__(options, formatter, decider)
        self.default_style_guide = FlakeHellStyleGuide(
            options, formatter, self.stats, decider=decider,
        )
        self.style_guides = [self.default_style_guide]
        self.style_guides.extend(self.populate_style_guides_with(options))

    @lru_cache(maxsize=None)
    def style_guide_for(self, filename: str):
        """Patched styleguide finder to give priority to flakehell's stileguides
        """
        guides = sorted(
            (g for g in self.style_guides if g.applies_to(filename)),
            key=lambda g: len(g.filename or ''),
            reverse=True,
        )
        for guide in guides:
            if isinstance(guide, FlakeHellStyleGuide):
                return guide
        return guides[0]

    def handle_error(
        self,
        code: str,
        filename: str,
        line_number: int,
        column_number: int,
        text: str,
        plugin: str,
        physical_line: str = None,
    ):
        guide = self.style_guide_for(filename)
        params = dict(
            code=code,
            filename=filename,
            line_number=line_number,
            column_number=column_number,
            text=text,
            physical_line=physical_line,
        )
        if isinstance(guide, FlakeHellStyleGuide):
            params['plugin'] = plugin
        return guide.handle_error(**params)


class FlakeHellStyleGuide(StyleGuide):
    def handle_error(
        self,
        code: str,
        filename: str,
        line_number: int,
        column_number: int,
        text: str,
        plugin: str,
        physical_line: str = None,
    ):
        """
        This function copied as is, but:
        1. Violation is replaced by FlakeHellViolation
        2. `error_is_selected` dropped. If we get here, the error IS selected.
        """
        disable_noqa = self.options.disable_noqa
        if not column_number:
            column_number = 0
        error = FlakeHellViolation(
            code=code,
            filename=filename,
            line_number=line_number,
            column_number=column_number + 1,
            text=text,
            physical_line=physical_line,
            plugin=plugin,
        )
        is_not_inline_ignored = error.is_inline_ignored(disable_noqa) is False
        is_included_in_diff = error.is_in(self._parsed_diff)
        if is_not_inline_ignored and is_included_in_diff:
            self.formatter.handle(error)
            self.stats.record(error)
            return 1
        return 0
