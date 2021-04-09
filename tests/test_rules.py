import pytest

from calrules.rules import Rule, Rules, Response


def test_rule():
    rule = Rule('from == "email@example.com"', 'from email@example.com')

    assert isinstance(rule, Rule)
    assert rule.pattern == 'from == "email@example.com"'


def test_rules():
    raw_rules = [
        {
            'pattern': 'from == "email@example.com"',
            'description': 'from email@example.com',
            'response': Response.ACCEPT
        },
        {
            'pattern': 'from == "other-email@example.com"',
            'description': 'from other-email@example.com'
        }
    ]

    rules = Rules(raw_rules)

    assert len(rules) == len(raw_rules)
    for r in rules:
        assert isinstance(r, Rule)
