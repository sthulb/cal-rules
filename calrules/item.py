from exchangelib.items.calendar_item import BaseMeetingItem

class Item:
    subject: str
    sender: str
    recipients: list[str]
    has_conflicts: bool
    sent_date   : int

    def __init__(self, item: BaseMeetingItem=None):
        self.hydrate(item)

    def hydrate(self, item: BaseMeetingItem=None):
        if item is None:
            raise ItemError('No item passed in')

        self.subject = item.subject
        self.sender = item.sender.email_address
        self.recipients = [to.email_address for to in item.to_recipients]
        self.has_conflicts = True if item.conflicting_meeting_count > 0 else False
        self.duration = item.duration
        self.modified = False if item.is_unmodified else True

    def to_dict(self):
        return {
            'subject': self.subject,
            'sender': self.sender,
            'recipients': self.recipients,
            'has_conflicts': self.has_conflicts,
            'duration': self.duration,
            'modified': self.modified
        }

    def delete(self):
        try:
            self.item.delete(affected_task_occurrences='AllOccurrences')
        except Exception as e:
            raise ItemError(e)

class ItemError(Exception):
    pass