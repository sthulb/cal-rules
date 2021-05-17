from enum import Enum

import re
import rule_engine

class Response(Enum):
    ACCEPT = 1
    MAYBE = 2
    DECLINE = 3
    DELETE = 4
    NOOP = 5

    @staticmethod
    def from_str(response):
        return Response[response.upper()]

class RuleRuntimeError(Exception):
    pass

class Rule:
    def __init__(self, pattern: str, description: str, response: Response = Response.DECLINE, *message: str):
        self.pattern = pattern
        self.description = description
        self.response = response
        self.message = message

        self.rule = rule_engine.Rule(
            pattern,
            rule_engine.Context(default_value=None, regex_flags=re.IGNORECASE | re.MULTILINE)
        )

    def matches(self, thing: dict) -> bool:
        try:
            return self.rule.matches(thing)
        except TypeError as e:
            raise RuleRuntimeError(e)
class Rules:
    def __init__(self, rules: list[dict]):
        self.load(rules)

    def __iter__(self):
        return iter(self.rules)

    def __next__(self):
        return next(self.rules)

    def __len__(self):
        return len(self.rules)

    def load(self, rules: list[dict]):
        _rules = []

        for r in rules:
            rule = Rule(
                pattern=r['pattern'],
                description=r['description']
            )

            if 'message' in r:
                rule.message = r['message']

            if 'response' in r:
                rule.response = Response.from_str(r['response'])

            _rules.append(rule)

        self.rules = _rules