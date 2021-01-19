import pytest

from calrules.rules import Rule, Rules

def test_rule():
  rule = Rule('from == "email@example.com"', 'from email@example.com')

  assert isinstance(rule, Rule)
  assert rule.pattern == 'from == "email@example.com"'

def test_rules():
  rules_yaml = [
    {
      'pattern': 'from == email@example.com',
      'description': 'from email@example.com'
    },
    {
      'pattern': 'from == other-email@example.com',
      'description': 'from other-email@example.com'
    }
  ]