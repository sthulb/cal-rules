import pytest

from calrules.item import Item, ItemError
from exchangelib.items.calendar_item import MeetingRequest

def test_item_init():
  item = Item()

  assert isinstance(item, Item)
