# Calendar Rules (calrules)

`calrules` enables you to perform actions against meeting requests and meeting cancellations.

`calrules` only works with Microsoft Exchange calendar providers.

## Installation
I'm too lazy to create a PyPi package, but you can easily install this using:
```sh
pip install git+https://github.com/sthulb/cal-rules.git
```
This package requires Python 3.9 or higher.

## Running
You can run the project using the `calrules` binary that's installed, make sure you include the `--config` parameter:
```sh
calrules --config /path/to/config.yaml
```

You can add more detailed logging using the `LOG_LEVEL=debug` env var.


## Rule attributes
- `sender` email address who sent the meeting
- `recipients` a list of email addresses the event was sent to.
- `type` meeting event type, `REQUEST` or `CANCELLATION`
- `subject` calendar event subject line
- `has_conflicts` if the event is conflicted with another
- `sent_date` a unix timestamp of sent date
- `duration` duration of the event
- `modified` if the event is an update to the original event

## Config
Example Config:
```yaml
exchange:
  email: <email>
  username: <username>
  domain: <domain>
  password: <password>
  server: <server>
  ca_cert: <optional mail server TLS root cert>

rules:
  - pattern: "type == 'CANCELLATION'"
    description: Meeting Cancellation
    response: DELETE

  - pattern: "sender == 'cal-spam@example.com'"
    description: Decline cal spam
    response: DECLINE
    message: No thanks!
    
  ## Complex rules
  - pattern: >
      sender in [
          "foo@example.com",
          "bar@example.com",
          "baz@example.com",
        ]
    description: Thing (Addresses)
    response: DECLINE 
  - pattern: >
      [s for s in [
          ".*Foo.*",
          ".*Bar.*",
          ".*Baz.*",
        ] if subject =~ s]
    description: Thing (Subject)
    response: DECLINE
```
