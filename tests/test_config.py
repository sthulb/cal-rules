import pytest

from yaml import safe_load
from calrules.config import loads_config, ConfigError

def test_loads_config():
  config_filename = 'tests/fixtures/loads_config.yaml'
  config = loads_config(config_filename)

  with open(config_filename) as f:
    raw_config = safe_load(f)

  assert config == raw_config

def test_loads_config_invalid_file():
  with pytest.raises(ConfigError):
    loads_config('tests/fixtures/loads_config_invalid.yaml')

def test_loads_config_file_not_found():
  with pytest.raises(FileNotFoundError):
    loads_config('not_a_real_file.yaml')
