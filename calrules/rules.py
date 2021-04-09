from enum import Enum

import re
import rule_engine

class Response(Enum):
  ACCEPT = 1
  MAYBE = 2
  DECLINE = 3
  DELETE = 4

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
    return self.rule.matches(thing)

class Rules:
  @classmethod
  def load(rules: list[Rule]) -> None:
    return Rules(rules)

  def __init__(self, rules: list[Rule]):
    self.load(rules)

  def __iter__(self):
    return iter(self.rules)

  def __next__(self):
    return next(self.rules)

  def __len__(self):
    return len(self.rules)

  def load(self, rules: list[Rule]):
    _rules = []

    for r in rules:
      rule = Rule(
        pattern=r['pattern'],
        description=r['description']
      )

      if 'response' in r:
        rule.decline = r['response']
      
      if 'message' in r:
        rule.decline = r['message']

      _rules.append(rule)

    self.rules = _rules