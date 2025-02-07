from yamale import make_schema, make_data, validate, YamaleError

SCHEMA = f"""
exchange:
  domain: str()
  username: str()
  password: str()
  server: str()
  port: int(required=False)
  email: str()
  ca_cert: str(required=False)
  days_back: int(required=False)

rules: list(include('rule'))

---

rule:
  pattern: str()
  description: str()
  response: enum('ACCEPT', 'MAYBE', 'DECLINE', 'DELETE', 'NOOP', required=False, none='NOOP')
  message: str(required=False)
"""


def loads_config(filename: str) -> dict:
    try:
        schema = make_schema(content=SCHEMA)
        data = make_data(filename)
    except FileNotFoundError as e:
        raise e

    try:
        validate(schema, data, strict=True, _raise_error=True)
    except YamaleError as e:
        raise ConfigError(e)

    return data.pop()[0]


class ConfigError(Exception):
    pass
