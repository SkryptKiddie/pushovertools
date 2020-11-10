# pushovertools
Scripts developed for use with pushover.net

## pushover.py
a python 3 module that can be imported and used to send messages to pushover.

## pushoverIpGrabber.py
Proof of Concept IP grabber using the pushoverModule to send the details

# how to import and use pushover module
```python
import pushover

# define the api key and user key
pushover.config.api_key = ""
pushover.config.user_key = ""

pushover.sendMessage(title="Example", message="Test message from pushover module", priority="-1")
```
