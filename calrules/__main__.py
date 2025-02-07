#!/usr/bin/env python

import logging
import os

from argparse import ArgumentParser

from calrules.config import loads_config, ConfigError
from calrules.exchange import Exchange
from calrules.rules import Response, Rules, RuleRuntimeError
from calrules.item import ItemActionError

for name in logging.root.manager.loggerDict:
    if not name.startswith("calrules"):
        logging.getLogger(name).setLevel(logging.WARNING)

logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=os.environ.get("LOG_LEVEL", "INFO").upper()
)

LOG = logging.getLogger(__name__)

args_parser = ArgumentParser(description="Calendar Rules")
args_parser.add_argument("--config", help="Path to config file")
args = args_parser.parse_args()

def main():
    config_file = "config.yaml"
    if hasattr(args, "config") and args.config is not None:
        config_file = args.config

    LOG.info(f"Using config file: {config_file}")

    LOG.info("Starting to scan mailbox")
    try:
        config = loads_config(config_file)
        LOG.debug(f"Loaded config: {config}")
    except ConfigError as e:
        LOG.error(f"Unable to parse config: {e}")

    exchange = Exchange(config["exchange"])
    items = exchange.items()
    rules = Rules(config["rules"])

    for i in items:
        for r in rules:
            try:
                match = r.matches(i.to_dict())
            except RuleRuntimeError as e:
                LOG.error(f"There was a problem running this rule: {r.description}")
                continue

            LOG.debug(f"Checking {i.subject} against {r.pattern}: {match}")
            LOG.debug("Item attributes: %s", i.to_dict())

            if match and i.action is not None:
                i.mark(r.response, r.message)
                LOG.debug(f"Marking {i.subject} with response: {r.message}.  Further processing of this item ceased.")
                break

    for i in items:
        LOG.info(f"Item: {i.subject} is marked for {i.action}")

        if i.action is Response.NOOP:
            continue

        try:
            if i.action is Response.ACCEPT:
                i.accept()
            elif i.action is Response.MAYBE:
                i.maybe()
            elif i.action is Response.DECLINE:
                i.decline()
            elif i.action is Response.DELETE:
                i.delete()
            else:
                LOG.warn(f"Unsure what to do, subject: {i.subject}, action: {i.action}")
        except ItemActionError as e:
            LOG.error(e)
