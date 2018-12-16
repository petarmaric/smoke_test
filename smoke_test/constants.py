import tempfile


PROGRAM_NAME = 'program.exe' # Normalize the compiled program name, so it works on all platforms
PROGRAM_TEST_DIR = tempfile.mkdtemp(prefix='smoke_test')

COMPILER_NAME = 'gcc'
COMPILER_SETTINGS = ['-g', '-o', PROGRAM_NAME]
LINKER_SETTINGS = ['-lm']

PROGRAM_POLL_TIME = 0.1 # Poll the running program status every X seconds
PROGRAM_MAX_WAIT_TIME = 3 # If not yet finished, terminate the program after X seconds run-time

FIXTURES_DIR = 'fixtures'
