#!/usr/bin/env python

from calrules.config import loads_config, ConfigError
from calrules.exchange import Exchange

def main():
  config = loads_config("./config.yaml")
  exchange = Exchange(config["exchange"])