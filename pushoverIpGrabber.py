import pushover, sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# define the api key and user key
pushover.config.api_key = ""
pushover.config.user_key = ""

class ReqHandler(BaseHTTPRequestHandler): 
    def do_GET(self):
        self.send_response(404, message="No content found")
        pushover.sendMessage(title="New connection", message=(str(self.headers)), priority="-1")
        self.end_headers()

httpServer = HTTPServer(("0.0.0.0", 80), ReqHandler)
    
try:
    print("Starting IP grabber, stop with ^C \n")
    httpServer.serve_forever()
except KeyboardInterrupt:
    print("Stopping...")
    sys.exit()
