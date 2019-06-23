from flake8.style_guide import DecisionEngine, StyleGuide, StyleGuideManager, Violation
from flake8.statistics import Statistics


class FlakeHellStyleGuideManager(StyleGuideManager):
    def __init__(self, options, formatter):
        self.options = options
        self.formatter = formatter
        self.stats = Statistics()
        self.decider = DecisionEngine(options)
        self.style_guides = []
        self.default_style_guide = FlakeHellStyleGuide(options, formatter, self.stats)
        self.style_guides = [self.default_style_guide] + list(self.populate_style_guides_with(options))


class FlakeHellStyleGuide(StyleGuide):
    def handle_error(self, code, filename, line_number, column_number, text, physical_line=None):
        disable_noqa = self.options.disable_noqa
        # NOTE(sigmavirus24): Apparently we're provided with 0-indexed column
        # numbers so we have to offset that here. Also, if a SyntaxError is
        # caught, column_number may be None.
        if not column_number:
            column_number = 0
        error = Violation(
            code,
            filename,
            line_number,
            column_number + 1,
            text,
            physical_line,
        )
        error_is_selected = (
            self.should_report_error(error.code) is Decision.Selected
        )
        is_not_inline_ignored = error.is_inline_ignored(disable_noqa) is False
        is_included_in_diff = error.is_in(self._parsed_diff)
        if (
            error_is_selected
            and is_not_inline_ignored
            and is_included_in_diff
        ):
            self.formatter.handle(error)
            self.stats.record(error)
            return 1
        return 0
