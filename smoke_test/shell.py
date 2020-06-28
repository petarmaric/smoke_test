import argparse
import logging
import os

from . import __version__
from .main import smoke_test
from .utils import get_test_stats


def main():
    # Setup command line option parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filename',
        help='Source code file to examine'
    )
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_const',
        const=logging.WARN,
        dest='verbosity',
        help='Be quiet, show only warnings and errors'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_const',
        const=logging.DEBUG,
        dest='verbosity',
        help='Be very verbose, show debug information'
    )
    parser.add_argument(
        '-e',
        '--error-code',
        action='store_const',
        const=True,
        dest='error_code',
        help='Return error code 1 if a test fails'
    )
    parser.add_argument(
        '--version',
        action='version',
        version="%(prog)s " + __version__
    )
    args = parser.parse_args()

    # Configure logging
    log_level = args.verbosity or logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s] %(message)s")

    results = smoke_test(args.filename)
    num_ok, num_failed, success_rate = get_test_stats(results)
    if log_level <= logging.INFO:
        logging.info("Test stats: ok = %d, failed = %d, success rate = %d %%", num_ok, num_failed, success_rate)
    else:
        print success_rate

    if args.error_code and num_failed:
        exit(1)


if __name__ == '__main__':
    main()
