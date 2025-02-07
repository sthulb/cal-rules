from enum import Enum
from calrules.rules import Response
from exchangelib.items.calendar_item import BaseMeetingItem, MeetingCancellation, MeetingRequest
from exchangelib.properties import MessageHeader

class ItemType(Enum):
    REQUEST = 1
    CANCELLATION = 2

class ItemError(Exception):
    pass

class ItemActionError(Exception):
    pass

class ItemThreadIndexError(Exception):
    pass

class Item:
    item: BaseMeetingItem

    type: ItemType

    subject: str
    sender: str
    recipients: list[str]
    has_conflicts: bool
    sent_date: int
    modified: bool
    duration: str

    action: Response

    def __init__(self, item: BaseMeetingItem = None):
        self.action = Response.NOOP
        self.item = item

        if item is not None:
            self.hydrate(item)

    def hydrate(self, item: BaseMeetingItem):
        if item is None:
            raise ItemError('No item passed in')

        if type(item) is MeetingRequest:
            self.type = ItemType.REQUEST
        elif type(item) is MeetingCancellation:
            self.type = ItemType.CANCELLATION
        else:
            raise ItemError("Type not known")

        self.subject = item.subject
        self.sender = item.sender.email_address
        if item.to_recipients is None and item.cc_recipients is None:
            to_recipients = []
        elif item.cc_recipients is None:
            to_recipients = item.to_recipients
        elif item.to_recipients is None:
            to_recipients = item.cc_recipients
        else:
            to_recipients = item.to_recipients + item.cc_recipients
        self.recipients = [to.email_address for to in to_recipients]

        if isinstance(item, MeetingRequest) and item.conflicting_meeting_count > 0:
            self.has_conflicts = True
        else:
            self.has_conflicts = False

        if isinstance(item, MeetingRequest):
            self.duration = item.duration

        self.modified = False if item.is_unmodified else True

    def mark(self, action: Response, message: str):
        self.action = action
        self.action_message = message

    def to_dict(self):
        item_type = "REQUEST" if self.type is ItemType.REQUEST else "CANCELLATION"

        return {
            'type': item_type,
            'subject': self.subject,
            'sender': self.sender,
            'recipients': self.recipients,
            'has_conflicts': self.has_conflicts,
            # 'duration': self.duration,
            'modified': self.modified
        }

    def delete(self):
        try:
            if self.item.associated_calendar_item_id:
                self.item.account.inbox.get(
                    id=self.item.associated_calendar_item_id.id,
                    changekey=self.item.associated_calendar_item_id.changekey
                ).delete()

            self.item.delete(affected_task_occurrences='AllOccurrences')
        except Exception as e:
            raise ItemActionError(e)

    def accept(self):
        try:
            self.item.accept()
        except Exception as e:
            raise ItemActionError(e)

    def decline(self):
        try:
            self.item.decline()
        except Exception as e:
            raise ItemActionError(e)

    def maybe(self):
        try:
            self.item.tentatively_accept()
        except Exception as e:
            raise ItemActionError(e)

    def thread_index(self) -> str:
        for h in self.item.headers:
                if h.name == "Thread-Index":
                    return h.value
