import logging
import os
import re
import subprocess
import shutil

from . import constants as c


def indent_string(s, indent=12):
    """
    Add the given number of space characters to the beginning every
    non-blank line in `s`, and return the result.
    """
    # This regexp matches the start of non-blank lines:
    return re.sub('(?m)^(?!$)', indent*' ', s)

def compile_source_code(filename):
    shutil.copy(filename, c.PROGRAM_TEST_DIR)

    process = subprocess.Popen(
        [c.COMPILER_NAME] + c.COMPILER_SETTINGS + [os.path.basename(filename)] + c.LINKER_SETTINGS,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        cwd=c.PROGRAM_TEST_DIR,
    )
    process.wait()
    stdout = process.stdout.read()
    stderr = process.stderr.read()

    if process.returncode != 0 or stdout or stderr:
        logging.fatal(
            "Can't compile source code:\n\treturn code: %d\n\tstdout:\n%s\n\tstderr:\n%s",
            process.returncode, indent_string(stdout), indent_string(stderr)
        )
        return False
    else:
        logging.info('Program compiled without errors nor warnings')
        return True

def cleanup_test_dir():
    logging.debug("Deleting the temporary testing directory '%s'", c.PROGRAM_TEST_DIR)
    shutil.rmtree(c.PROGRAM_TEST_DIR)

def get_test_stats(results):
    if not results:
        return 0, 0, 0 # num_ok, num_failed, success_rate

    num_total = len(results)

    num_ok = sum(results.values())
    num_failed = num_total - num_ok
    success_rate = int(round(100.0 * num_ok / num_total))

    return num_ok, num_failed, success_rate
