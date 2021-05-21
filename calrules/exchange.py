import logging

from calrules.item import Item
from calrules.exchange_rootca import ExchangeRootCA

from pathlib import Path

from exchangelib.account import Account, DELEGATE
from exchangelib.configuration import Configuration
from exchangelib.credentials import Credentials
from exchangelib.items import MeetingCancellation, MeetingRequest
from exchangelib.protocol import BaseProtocol
from exchangelib import EWSDateTime, Q
from datetime import timedelta

LOG = logging.getLogger(__name__)

class Exchange:
    def __init__(self, exchange: dict) -> None:
        port = 443
        if "port" in exchange:
            port = exchange["port"]

        try:
            creds = Credentials(f'{exchange["domain"]}\{exchange["username"]}', exchange["password"])
            config = Configuration(server=exchange["server"], port=port, credentials=creds)

            if "ca_cert" in exchange and Path(exchange["ca_cert"]).is_file():
                LOG.info(f"CA Path: {exchange['ca_cert']}")
                ExchangeRootCA.ca_cert = exchange["ca_cert"]
                BaseProtocol.HTTP_ADAPTER_CLS = ExchangeRootCA

            if "days_back" in exchange:
                self.days_back = exchange["days_back"]

            self.account = Account(exchange['email'], autodiscover=False, config=config, access_type=DELEGATE)
        except Exception as e:
            print(e)

    def items(self):
        items = []
        seen_threads = []

        try:
            start = self.account.default_timezone.localize(EWSDateTime.today() - timedelta(days=self.days_back))
            messageFilter = Q(datetime_received__gte=start)
            LOG.info(f"Processing only items received after: {start}")
        except AttributeError:
            messageFilter = Q()

        for item in self.account.inbox.all().order_by("-datetime_received").filter(messageFilter):
            if not isinstance(item, MeetingRequest) and not isinstance(item, MeetingCancellation):
                continue

            hydrated_item = Item(item)

            # check to see if we've seen this thread before, skip it if we have
            thread_index = hydrated_item.thread_index()
            if thread_index in seen_threads:
                continue
            else:
                seen_threads.append(thread_index)

            LOG.debug(f"item: {hydrated_item.to_dict}")
            items.append(hydrated_item)

        return items
