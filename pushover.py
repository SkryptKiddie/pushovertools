import argparse, requests, os, sys
from sys import exit

parser = argparse.ArgumentParser(description="Pushover message relayer")
parser.add_argument("title", type=str, help="message title")
parser.add_argument("msg", type=str, help="message body")
parser.add_argument("priority", type=int, help="priority, valid options are -2, -1, 1 or 2")
args = parser.parse_args()

class pushoverauth:
    api_key = "" # pushover application key
    user_key = "" # recipient user key

def sendMessage():
    print("Sending message...")
    body = {
        "token": pushoverauth.api_key,
        "user": pushoverauth.user_key,
        "title": str(args.title),
        "message": str(args.msg),
        "priority": str(args.priority)
    }
    response = requests.post("https://api.pushover.net/1/messages.json", body, verify=False)
    if (str(response)[10:-1]) == "[200]":
        print("Message sent!")
        sys.exit()
    else:
        print("An error occured and your message was not sent.")
        sys.exit()

print("Pushover message pusher")
sendMessage()
