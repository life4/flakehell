# built-in
import json
import re
from collections import defaultdict
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Dict, List, Set

# app
from .._constants import NAME, VERSION


CODE = '[a-z]+[0-9]+'
SEP = r'[,\s]+'


class YesQA:
    noqa_file_re = re.compile(r'^# flake8[:=]\s*noqa', re.I)
    noqa_re = re.compile(f'# noqa(: ?{CODE}({SEP}{CODE})*)?', re.I)
    code_re = re.compile(CODE, re.I)

    def get_ignored_codes(self, line: str) -> List[str]:
        match = self.noqa_re.search(line)
        if not match:
            return []
        comment = match.group()
        return self.code_re.findall(comment)

    def remove_noqa(self, line: str) -> str:
        if self.noqa_file_re.match(line):
            return ''
        match = self.noqa_re.search(line)
        if not match:
            return line
        line = line[:match.start()] + line[match.end():]
        return line.rstrip()

    def remove_noqa_code(self, line: str, code: str) -> str:
        match = self.noqa_re.search(line)
        if not match:
            return line
        comment = match.group()
        codes = self.code_re.findall(comment)

        # if it was only one code and we remove it, remove the comment at all
        if codes == [code]:
            return self.remove_noqa(line)

        # remove only one code from the list of codes
        codes = [c for c in codes if c != code]
        new_comment = '# noqa: ' + ', '.join(codes)
        line = line[:match.start()] + new_comment + line[match.end():]
        return line.rstrip()

    def get_errors(self, path: Path, noqa: bool) -> Dict[int, Set[str]]:
        from .._patched import FlakeHellApplication

        app = FlakeHellApplication(program=NAME, version=VERSION)
        output = StringIO()
        cmd = ['--format', 'json', str(path)]
        if not noqa:
            cmd.append('--disable-noqa')
        with redirect_stdout(output):
            app.run(cmd)
        output.seek(0)

        result = defaultdict(set)
        for line in output:
            data = json.loads(line)
            result[data['line']].add(data['code'])
        return dict(result)

    def remove_unused_codes(self, content: str, errors: Dict[int, Set[str]]) -> str:
        result = []
        for line_number, line in enumerate(content.split('\n'), 1):
            ignored_codes = self.get_ignored_codes(line)
            actual_codes = errors.get(line_number, set())
            for code in ignored_codes:
                if code not in actual_codes:
                    line = self.remove_noqa_code(line=line, code=code)
            result.append(line)
        return '\n'.join(result)

    def get_modified_file(self, path: Path, original: str) -> str:
        old_errors = self.get_errors(path=path, noqa=True)
        all_errors = self.get_errors(path=path, noqa=False)
        new_errors = dict()
        for line_number, codes in all_errors.items():
            new_codes = codes - old_errors.get(line_number, set())
            if new_codes:
                new_errors[line_number] = new_codes

        return self.remove_unused_codes(content=original, errors=new_errors)

    def __call__(self, path: Path) -> bool:
        original = path.read_text(encoding='utf-8')
        modified = self.get_modified_file(path=path, original=original)
        if modified == original:
            return False
        path.write_text(modified)
        return True
