import logging
import os

from ... import constants as c
from ...utils import indent_string
from . import mixins
from .base import BaseFunctionalTest


class BaseFileTest(BaseFunctionalTest):
    def _setup(self, *args, **kwargs):
        super(BaseFileTest, self)._setup(*args, **kwargs)

        self.input_filename = self.fixture_id + '.in'
        self.output_filename = self.fixture_id + '.out'

        self.args_template_context = {
            'input_filename': self.input_filename,
            'output_filename': self.output_filename,
        }

        self.original_filenames = os.listdir(c.PROGRAM_TEST_DIR)
        logging.debug("Recording the existing filenames before running test: %s", self.original_filenames)

        with open(os.path.join(c.PROGRAM_TEST_DIR, self.input_filename), 'w') as out:
            logging.debug("Copying input file contents to '%s'", self.input_filename)
            out.write(self.input)

    def _teardown(self):
        super(BaseFileTest, self)._teardown()

        for filename in set(os.listdir(c.PROGRAM_TEST_DIR)) - set(self.original_filenames):
            logging.debug("Cleaning up after running test, removing '%s'", filename)
            os.remove(os.path.join(c.PROGRAM_TEST_DIR, filename))


class BaseFileTextTest(BaseFileTest):
    def _check_program_stdout(self, stdout):
        return stdout == ''

    def _analyze_program_output(self, stdout, stderr, returncode):
        output_file_path = os.path.join(c.PROGRAM_TEST_DIR, self.output_filename)
        if not os.path.exists(output_file_path):
            return self._fail("Program failed to create '%s'" % self.output_filename)

        with open(output_file_path) as fp_got:
            got = fp_got.read()
            return self._pass_or_fail(
                pass_condition=(self.normalize_output(self.expected_output) == self.normalize_output(got)),
                fail_message="\n\tExpected:\n%s\tGot:\n%s" % (indent_string(self.expected_output), indent_string(got))
            )


class FileTextWhitespaceSensitiveTest(BaseFileTextTest): pass
class FileTextTest(mixins.NormalizeWhitespacesMixin, BaseFileTextTest): pass
class FileNumbersTest(mixins.NormalizeToLineEndingNumbersMixin, BaseFileTextTest): pass


class BaseFileErrorHandlingTest(BaseFileTest):
    def _check_program_stdout(self, stdout):
        return True

    def _analyze_program_output(self, stdout, stderr, returncode):
        return self._pass()


class FileErrorInputNotReadableTest(BaseFileErrorHandlingTest): pass
class FileErrorOutputNotWritableTest(BaseFileErrorHandlingTest): pass
