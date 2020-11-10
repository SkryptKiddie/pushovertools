import requests, os, sys
class pushoverConfig(): # pushover module in python3
    def __init__(self):
        self.api_key = "" # api key, should be defined in the main program
        self.user_key = "" # user key, should also be defined in the main program
        self.api_endpoint = "https://api.pushover.net/1/messages.json" # pushover API endpoint
        self.verify_ssl = False # define whether to check SSL

config = pushoverConfig() # define config class

def sendMessage(title, message, priority):
    """Send a normal text message with a title, body and priority."""
    body = {
        "token": config.api_key,
        "user": config.user_key,
        "title": str(title), # message title
        "message": str(message), # message body
        "priority": str(priority)} # message priority, valid options are -2 -1 1 2
    response = requests.post(config.api_endpoint, body, verify=config.verify_ssl)
    if (str(response)[10:-1]) == "[200]":
        return True # success
    else:
        return False # error

def sendAttachment(title, message, attachment, priority):
    """Send a message with a title, body, attachment and priority. Attachment must contain Content-Disposition and Content-Type headers."""
    body = {
        "token": config.api_key,
        "user": config.user_key,
        "title": str(title), # message title
        "message": str(message), # message body
        "attachment": str(attachment), # message attachment
        "priority": str(priority)} # message priority
    response = requests.post(config.api_endpoint, body, verify=config.verify_ssl)
    if (str(response)[10:-1]) == "[200]":
        return True # success
    else:
        return False # error

def checkRatelimit():
    """Check how many requests you have made to the API with your API key."""
    response = requests.get("https://api.pushover.net/1/apps/limits.json?token={}".format(config.api_key), verify=config.verify_ssl)
    if response.status_code == 200:
        return str(response.json())
    else:
        return "Bad token was passed"
    
