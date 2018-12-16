import logging

from . import constants as c
from .fixtures import load_fixtures_from
from .tests import BaseTest
from .utils import cleanup_test_dir, compile_source_code


def smoke_test(filename, skip_test_dir_cleanup=False):
    results = {}
    if compile_source_code(filename):
        for fixture_name, fixture_id, fixture_data in load_fixtures_from(c.FIXTURES_DIR):
            test = BaseTest.coerce(fixture_name)
            results[test.test_id(fixture_id)] = test(filename, fixture_id, fixture_data)

    if not skip_test_dir_cleanup:
        cleanup_test_dir()

    return results
