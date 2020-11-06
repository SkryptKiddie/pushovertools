import requests
class pushovermodule: # basic pushover integration for any python3 script
    def __init__(self):
        self.api_key = "" # pushover application key
        self.user_key = "" # recipient user key

    def sendMessage(self, title, message, priority):
        body = {
        "token": self.api_key,
        "user": self.user_key,
        "title": str(title), # message title
        "message": str(message), # message body
        "priority": str(priority)} # message priority, valid options are -2 -1 1 2
        response = requests.post("https://api.pushover.net/1/messages.json", body, verify=False)
        if (str(response)[10:-1]) == "[200]":
            return True # success
        else:
            return False # error

pushover = pushovermodule() # define pushover class
pushover.sendMessage(title="Example", message="Test message from pushover module", priority="-1") # example function call
