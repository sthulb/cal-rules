# Calendar Rules (calrules)

`calrules` enables you to perform actions against meeting requests and meeting cancellations.

`calrules` only works with Microsoft Exchange calendar providers.

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
```

## Running
