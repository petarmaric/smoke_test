from contextlib import contextmanager
import logging
import re

from friendly_name_mixin import FriendlyNameFromClassMixin
from simple_plugins import PluginMount


class BaseTest(FriendlyNameFromClassMixin):
    _fixture_name_re = re.compile('( Test$)')

    __metaclass__ = PluginMount

    class Meta:
        id_field = 'fixture_name'
        id_field_coerce = str

    def __str__(self):
        return self.fixture_name

    @property
    def fixture_name(self):
        if not hasattr(self, '_fixture_name'):
            base_name = self._fixture_name_re.sub('', self.name)
            self._fixture_name = '-'.join(base_name.lower().split())

        return self._fixture_name

    def test_id(self, fixture_id):
        return "%s:%s" % (self.fixture_name, fixture_id)

    def _format_message(self, base, extra=None):
        return base if not extra else "%s: %s" % (base, extra)

    def _pass(self, message=None):
        logging.info(self._format_message("PASSED test '%s'" % self.test_id(self.fixture_id), message))
        return True

    def _fail(self, message=None):
        logging.error(self._format_message("FAILED test '%s'" % self.test_id(self.fixture_id), message))
        return False

    def _pass_or_fail(self, pass_condition, pass_message=None, fail_message=None):
        return self._pass(pass_message) if pass_condition else self._fail(fail_message)

    def _setup(self, source_code_filename, fixture_id, fixture_data):
        logging.debug("Preparing the environment to run test '%s'...", self.test_id(fixture_id))

        self.source_code_filename = source_code_filename
        self.fixture_id = fixture_id
        self.fixture_data = fixture_data

    def _teardown(self):
        logging.debug("Cleaning up the environment after running test '%s'...", self.test_id(self.fixture_id))

    @contextmanager
    def _test_environment(self, source_code_filename, fixture_id, fixture_data):
        try:
            self._setup(source_code_filename, fixture_id, fixture_data)
            yield
        finally:
            self._teardown()

    def _test(self):
        raise NotImplementedError

    def test(self, source_code_filename, fixture_id, fixture_data):
        with self._test_environment(source_code_filename, fixture_id, fixture_data):
            return bool(self._test())

    def __call__(self, source_code_filename, fixture_id, fixture_data):
        return self.test(source_code_filename, fixture_id, fixture_data)
