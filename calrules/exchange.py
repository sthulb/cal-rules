# from calrules.config import Config

from calrules.item import Item, ItemError

import logging

from exchangelib.account import Account, DELEGATE
from exchangelib.configuration import Configuration
from exchangelib.credentials import Credentials
from exchangelib.items import MeetingCancellation, MeetingRequest

LOGGER_NAME = "exchange"

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

class Exchange:
    def __init__(self, exchange: dict) -> None:
        creds = Credentials(f'{exchange["domain"]}\{exchange["username"]}', exchange["password"])
        config = Configuration(server=exchange["server"], credentials=creds)

        self.account = Account(exchange['email'], autodiscover=False, config=config, access_type=DELEGATE)

    def items(self):
        items = []
        for item in self.account.inbox.all():
            if not isinstance(item, MeetingCancellation) or not isinstance(item, MeetingRequest):
                continue

            logger.info(f'Got item: {item.subject}')

            items.append(Item(item))

        return items
