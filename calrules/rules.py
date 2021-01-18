from __future__ import annotations

import re
import rule_engine

class Rule:
  def __init__(self, pattern: str, description: str, decline: bool = True, *decline_message: str):
    self.pattern = pattern
    self.description = description
    self.decline = decline
    self.decline_message = decline_message

    self.rule = rule_engine.Rule(
      pattern, 
      rule_engine.Context(default_value=None, regex_flags=re.IGNORECASE | re.MULTILINE)
    )

  def __getattribute__(self, name: str) -> Any:
      return super().__getattribute__(name)

  def __setattr__(self, name: str, value: Any) -> None:
      return super().__setattr__(name, value)

  def matches(self, thing: dict) -> bool:
    return self.rule.matches(thing)

class Rules:
  @classmethod
  def load(rules: list[Rule]) -> Rules:
    return Rules(rules)

  def __init__(self, rules: list[Rule]):
    self.load(rules)

  def __iter__(self):
    return iter(self.rules)

  def __next__(self):
    return next(self.rules)

  def load(self, rules: list[Rule]):
    _rules = []

    for r in rules:
      rule = Rule(
        pattern=r['pattern'],
        description=r['description']
      )

      if 'decline' in r:
        rule.decline = r['decline']
      
      if 'decline_message' in r:
        rule.decline = r['decline_message']

      _rules.append(rule)

    self.rules = _rules