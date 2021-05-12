# from calrules.config import Config

from calrules.item import Item, ItemError
from calrules.exchange_rootca import ExchangeRootCA

import logging

from pathlib import Path

from exchangelib.account import Account, DELEGATE
from exchangelib.configuration import Configuration
from exchangelib.credentials import Credentials
from exchangelib.items import MeetingCancellation, MeetingRequest
from exchangelib.protocol import BaseProtocol
from exchangelib.errors import TransportError
from exchangelib.version import Version, Build

from pprint import pprint

LOGGER_NAME = "exchange"

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

class Exchange:
    def __init__(self, exchange: dict) -> None:
        try:
            creds = Credentials(f'{exchange["domain"]}\{exchange["username"]}', exchange["password"])
            config = Configuration(server=exchange["server"], credentials=creds, version=Version(build=Build(14, 3, 513)))

            if "ca_cert" in exchange and Path(exchange["ca_cert"]).is_file():
                logger.info(f"CA Path: {exchange['ca_cert']}")
                ExchangeRootCA.ca_cert = exchange["ca_cert"]
                BaseProtocol.HTTP_ADAPTER_CLS = ExchangeRootCA

            self.account = Account(exchange['email'], autodiscover=False, config=config, access_type=DELEGATE)
        except Exception as e:
            print(e)

    def items(self):
        items = []
        for item in self.account.root.all():
            if not isinstance(item, MeetingCancellation) or not isinstance(item, MeetingRequest):
                continue

            logger.info(f"Got item: {item.subject}")

            items.append(Item(item))

        return items
