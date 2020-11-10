from typing import NamedTuple
import requests, urllib3
from datetime import datetime

class pushoverConfig(): # pushover module in python3
    def __init__(self):
        self.api_key = "" # api key, should be defined in the main program
        self.user_key = "" # user key, should also be defined in the main program
        self.group_key = "" # group key, should also be defined in the main program if needed
        self.api_endpoint = "https://api.pushover.net/1/messages.json" # pushover API endpoint
        self.verify_ssl = True # define whether to check SSL

config = pushoverConfig() # define config class

class main:
    def sendMessage(dest, title, message, priority):
        """Send a normal text message with a title, body and priority."""
        body = {
            "token": config.api_key,
            "user": str(dest),
            "title": str(title), # message title
            "message": str(message), # message body
            "priority": str(priority)} # message priority, valid options are -2 -1 1 2
        response = requests.post(config.api_endpoint, body, verify=config.verify_ssl)
        if (str(response)[10:-1]) == "[200]":
            return response.json()
        else:
            return False # error

    def sendAttachment(dest, title, message, attachment, priority):
        """Send a message with a title, body, attachment and priority. Attachment must contain Content-Disposition and Content-Type headers."""
        body = {
            "token": config.api_key,
            "user": str(dest),
            "title": str(title), # message title
            "message": str(message), # message body
            "attachment": str(attachment), # message attachment
            "priority": str(priority)} # message priority
        response = requests.post(config.api_endpoint, body, verify=config.verify_ssl)
        if (str(response)[10:-1]) == "[200]":
            return True # success
        else:
            return False # error

    def sendPriorityMessage(dest, title, message, retry, expire):
        """Send an emergency priority message."""
        body = {
            "token": config.api_key,
            "user": str(dest),
            "title": str(title), # message title
            "message": str(message), # message body
            "priority": "2",
            "retry": str(retry),
            "expire": str(expire)}
        response = requests.post(config.api_endpoint, body, verify=config.verify_ssl)
        if response.status_code == 200:
            return "Message receipt ID: " + str(response.json()["receipt"])
        else:
            return False # error


    def checkRatelimit():
        """Check how many requests you have made to the API with your API key."""
        response = requests.get("https://api.pushover.net/1/apps/limits.json?token={}".format(config.api_key), verify=config.verify_ssl)
        if response.status_code == 200:
            limit = "Message limit: {}".format(response.json()["limit"])
            remaining = "Messages remaining: {}".format(response.json()["remaining"])
            reset_ts = int(response.json()["reset"])
            ts = datetime.utcfromtimestamp(reset_ts).strftime('%Y-%m-%d %H:%M:%S')
            reset = "Limit resets at: {}".format(ts)
            return "{}\n{}\n{}".format(limit, remaining, reset)
        else:
            return "Bad token was passed"

    def checkReceipt(reciept):
        """Check pushover emergency priority message receipt status."""
        response = requests.get("https://api.pushover.net/1/receipts/{}.json?token={}".format(reciept, config.api_key), verify=config.verify_ssl)
        if response.json()["acknowledged"] == 1:
            ack_ts = int(response.json()["acknowledged_at"])
            ts = datetime.utcfromtimestamp(ack_ts).strftime('%Y-%m-%d %H:%M:%S')
            return "Message was acknowledged at {} by {}.".format(ts, response.json()["acknowledged_by_device"])
        else:
            await_ack_ts = int(response.json()["last_delivered_at"])
            ts = datetime.utcfromtimestamp(await_ack_ts).strftime('%Y-%m-%d %H:%M:%S')
            return "Message has not been acknowledged. Last retried at {}.".format()

    def validateUser(user):
        """Validate a user associated with your application."""
        body = {
            "token": config.api_key,
            "user": str(user)}
        response = requests.post("https://api.pushover.net/1/users/validate.json", body, verify=config.verify_ssl)
        if response.json()["status"] == 1:
            devices = "Devices: {}".format(response.json()["devices"])
            licenses = "Licenses: {}".format(response.json()["licenses"])
            return "{}\n{}".format(devices, licenses)
        else:
            return "User not found"

class group:
    def groupDetails():
        """Get details about a Pushover delivery group."""
        response = requests.get("https://api.pushover.net/1/groups/{}.json?token={}".format(config.group_key, config.api_key), verify=config.verify_ssl)
        if response.status_code == 200:
            name = "Group name: " + response.json()["name"]
            users = "User count: " + len(response.json()["users"])
            return "{}\n{}".format(name, users)
        else:
            return "Bad token was passed"

    def addUser(user, memo):
        """Add a user to a Pushover delivery group."""
        body = {
            "token": config.api_key,
            "user": str(user),
            "memo": str(memo)}
        response = requests.post("https://api.pushover.net/1/groups/{}/add_user.json?token={}".format(config.group_key, config.api_key), body, verify=config.verify_ssl)
        if response.status_code == 200:
            return str(response.json())
        else:
            return "Bad group key or API key was passed, or requested user was not found."

    def deeteUser(user):
        """Remove a user from a Pushover delivery group."""
        body = {
            "token": config.api_key,
            "user": str(user)}
        response = requests.post("https://api.pushover.net/1/groups/{}/delete_user.json?token={}".format(config.group_key, config.api_key), body, verify=config.verify_ssl)
        if response.status_code == 200:
            return str(response.json())
        else:
            return "Bad group key or API key was passed, or requested user was not found."

    def enableUser(user):
        """Enable a disabled user from a Pushover delivery group."""
        body = {
            "token": config.api_key,
            "user": str(user)}
        response = requests.post("https://api.pushover.net/1/groups/{}/enable_user.json?token={}".format(config.group_key, config.api_key), body, verify=config.verify_ssl)
        if response.status_code == 200:
            return str(response.json())
        else:
            return "Bad group key or API key was passed, or requested user was not found."

    def disableUser(user):
        """Disable a user from a Pushover delivery group."""
        body = {
            "token": config.api_key,
            "user": str(user)}
        response = requests.post("https://api.pushover.net/1/groups/{}/disable_user.json?token={}".format(config.group_key, config.api_key), body, verify=config.verify_ssl)
        if response.status_code == 200:
            return str(response.json())
        else:
            return "Bad group key or API key was passed, or requested user was not found."

    def renameGroup(name):
        """Rename a Pushover delivery group."""
        body = {
            "token": config.api_key,
            "name": str(name)}
        response = requests.post("https://api.pushover.net/1/groups/{}/rename.json?token={}".format(config.group_key, config.api_key), body, verify=config.verify_ssl)
        if response.status_code == 200:
            return str(response.json())
        else:
            return "Bad group key or API key was passed."

