from ...utils import indent_string
from . import mixins
from .base import BaseFunctionalTest


class BaseStdioTest(BaseFunctionalTest):
    def _check_program_stdout(self, stdout):
        return True

    def _analyze_program_output(self, stdout, stderr, returncode):
        return self._pass_or_fail(
            pass_condition=(self.normalize_output(self.expected_output) == self.normalize_output(stdout)),
            fail_message="\n\tExpected:\n%s\tGot:\n%s" % (indent_string(self.expected_output), indent_string(stdout))
        )

    def _create_process(self):
        process = super(BaseStdioTest, self)._create_process()
        process.stdin.write(self.input)

        return process


class StdioTextWhitespaceSensitiveTest(BaseStdioTest): pass
class StdioTextTest(mixins.NormalizeWhitespacesMixin, BaseStdioTest): pass
class StdioNumbersTest(mixins.NormalizeToLineEndingNumbersMixin, BaseStdioTest): pass
