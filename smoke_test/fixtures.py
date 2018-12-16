import fnmatch
import os

import yaml

from .tests import BaseTest


def find_filenames(path, filename_pattern):
    file_list = sorted(os.listdir(path))
    for name in fnmatch.filter(file_list, filename_pattern):
        yield os.path.join(path, name)

def get_fixture_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def validate_fixture_filenames(filenames):
    for filename in filenames:
        BaseTest.coerce(get_fixture_name(filename))
        yield filename

def open_fixture_files(filenames):
    for filename in filenames:
        with open(filename, 'r') as fp:
            yield filename, yaml.load(fp)

def parse_fixture_files(fixture_files):
    for filename, fixtures in fixture_files:
        fixture_name = get_fixture_name(filename)
        for fixture_id, fixture_data in sorted(fixtures.items()):
            yield fixture_name, fixture_id, fixture_data

def load_fixtures_from(fixtures_dir):
    fixture_filenames = find_filenames(fixtures_dir, '*.yaml')
    fixture_filenames = validate_fixture_filenames(fixture_filenames)
    fixture_files = open_fixture_files(fixture_filenames)
    fixtures = parse_fixture_files(fixture_files)

    return fixtures
