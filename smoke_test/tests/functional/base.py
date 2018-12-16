from datetime import datetime, timedelta
import logging
import os
from string import Template
import subprocess
from time import sleep

from ... import constants as c
from ...utils import indent_string
from ..base import BaseTest


class BaseFunctionalTest(BaseTest):
    def _setup(self, *args, **kwargs):
        super(BaseFunctionalTest, self)._setup(*args, **kwargs)

        self.args = self.fixture_data.get('args', '')
        self.args_template_context = {}

        self.input = self.fixture_data.get('input', '')

        self.expected_output = self.fixture_data.get('expected-output', '')
        self.expected_returncode = self.fixture_data.get('expected-returncode', 0)

    def normalize_output(self, s):
        return s

    def _check_program_stdout(self, stdout):
        raise NotImplementedError

    def _check_program_stderr(self, stderr):
        return stderr == ''

    def _check_program_returncode(self, returncode):
        return returncode == self.expected_returncode

    def _sanity_check(self, stdout, stderr, returncode):
        if self._check_program_returncode(returncode) and self._check_program_stderr(stderr) and self._check_program_stdout(stdout):
            return True

        return self._fail(
            "Program terminated with errors:\n\treturn code: %d (expected %d)\n\tstdout:\n%s\n\tstderr:\n%s" % (
                returncode, self.expected_returncode, indent_string(stdout), indent_string(stderr)
            )
        )

    def _analyze_program_output(self, stdout, stderr, returncode):
        raise NotImplementedError

    def _resolve_args(self):
        return Template(self.args).substitute(self.args_template_context)

    def _create_process(self):
        process = subprocess.Popen(
            [os.path.join(c.PROGRAM_TEST_DIR, c.PROGRAM_NAME)] + self._resolve_args().split(),
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=c.PROGRAM_TEST_DIR,
        )

        return process

    def _test(self):
        process = self._create_process()

        start_time = datetime.now()
        while process.poll() is None:
            if datetime.now() - start_time > timedelta(seconds=c.PROGRAM_MAX_WAIT_TIME):
                process.terminate()
                return self._fail("Program took more than %d seconds to complete!" % c.PROGRAM_MAX_WAIT_TIME)

            logging.debug("Waiting for the program to complete...")
            sleep(c.PROGRAM_POLL_TIME)

        stdout = process.stdout.read()
        stderr = process.stderr.read()
        returncode = process.returncode
        if self._sanity_check(stdout, stderr, returncode):
            return self._analyze_program_output(stdout, stderr, returncode)
