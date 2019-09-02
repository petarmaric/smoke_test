About
=====

Console app and Python API for automated smoke testing, preconfigured to make
coursework easier for our `ACS`_ students.

.. _`ACS`: http://www.acs.uns.ac.rs/

Installation
============

To install smoke_test run::

    $ pip install smoke_test

Console app usage
=================

Quick start::

    $ smoke_test <filename>

Show help::

    $ smoke_test --help

Python API usage
================

Quick start::

    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    >>> import os
    >>> os.chdir('examples/file')

    >>> from smoke_test.main import smoke_test
    >>> from smoke_test.utils import get_test_stats

    >>> results = smoke_test('program-error-bad-function-calls-count.c')
    >>> num_ok, num_failed, success_rate = get_test_stats(results)
    >>> logging.info("Test stats: ok = %d, failed = %d, success rate = %d %%", num_ok, num_failed, success_rate)

Contribute
==========

If you find any bugs, or wish to propose new features `please let us know`_.

If you'd like to contribute, simply fork `the repository`_, commit your changes
and send a pull request. Make sure you add yourself to `AUTHORS`_.

.. _`please let us know`: https://github.com/petarmaric/smoke_test/issues/new
.. _`the repository`: https://github.com/petarmaric/smoke_test
.. _`AUTHORS`: https://github.com/petarmaric/smoke_test/blob/master/AUTHORS
