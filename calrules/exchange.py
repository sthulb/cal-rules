import logging

from calrules.logger import logger
from calrules.item import Item, ItemError
from calrules.exchange_rootca import ExchangeRootCA

from pathlib import Path

from exchangelib.account import Account, DELEGATE
from exchangelib.configuration import Configuration
from exchangelib.credentials import Credentials
from exchangelib.items import MeetingCancellation, MeetingRequest
from exchangelib.protocol import BaseProtocol

from pprint import pprint

LOG = logging.getLogger(__name__)

class Exchange:
    def __init__(self, exchange: dict) -> None:
        try:
            creds = Credentials(f'{exchange["domain"]}\{exchange["username"]}', exchange["password"])
            config = Configuration(server=exchange["server"], credentials=creds)

            if "ca_cert" in exchange and Path(exchange["ca_cert"]).is_file():
                LOG.info(f"CA Path: {exchange['ca_cert']}")
                ExchangeRootCA.ca_cert = exchange["ca_cert"]
                BaseProtocol.HTTP_ADAPTER_CLS = ExchangeRootCA

            self.account = Account(exchange['email'], autodiscover=False, config=config, access_type=DELEGATE)
        except Exception as e:
            print(e)

    def items(self):
        items = []
        for item in self.account.inbox.all():
            if not isinstance(item, MeetingRequest) and not isinstance(item, MeetingCancellation):
                continue

            hydrated_item = Item(item)

            LOG.debug(f"item: {hydrated_item.to_dict}")
            items.append(hydrated_item)

        return items
