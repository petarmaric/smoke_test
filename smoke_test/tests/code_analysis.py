import hashlib
import logging

from pycparser import c_ast, parse_file
from pycparserext.ext_c_parser import GnuCParser

from .base import BaseTest


class BaseSourceCodeAnalysisTest(BaseTest):
    _ast_cache = {}

    @property
    def ast(self):
        with open(self.source_code_filename) as fp:
            file_hash = hashlib.sha1(fp.read()).hexdigest()

        if file_hash not in self._ast_cache:
            self._ast_cache[file_hash] = parse_file(
                self.source_code_filename,
                use_cpp=True,
                parser=GnuCParser(),
            )

        return self._ast_cache[file_hash]

    def _setup(self, *args, **kwargs):
        super(BaseSourceCodeAnalysisTest, self)._setup(*args, **kwargs)
        self.ast # HACK: A NO-OP used to activate the `_ast_cache` while we're still in the `_setup` stage


class CountFunctionCallsTest(BaseSourceCodeAnalysisTest):
    class FuncCallVisitor(c_ast.NodeVisitor):
        def __init__(self, function_name):
            self.function_name = function_name
            self.count = 0

        def visit_FuncCall(self, node):
            if node.name.name == self.function_name:
                logging.debug("'%s' function call found at %s", self.function_name, node.name.coord)
                self.count += 1

            self.generic_visit(node)

    def _test(self):
        function_name = self.fixture_id
        expected = self.fixture_data

        visitor = self.FuncCallVisitor(self.fixture_id)
        visitor.visit(self.ast)
        got = visitor.count

        return self._pass_or_fail(
            pass_condition=(expected == got),
            fail_message="There should be %d '%s' function call(s) in the source code (%d found)" % (expected, function_name, got)
        )
