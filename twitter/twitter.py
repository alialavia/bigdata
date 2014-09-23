from twython import TwythonStreamer

APP_KEY = "Cr0DUzVu5vCL1Ocv0J9TzgXS8"
APP_SECRET = "HyS4V5QiWCsrzXHGuYQao4Vi7NUwLGeID9RzV2i4sf6YmPQdXd"

OAUTH_TOKEN = "2826918072-iRPfA5QUzGWBSvAxXz77V2J8vbrFQMp5FdPENoF"
OAUTH_TOKEN_SECRET = "TY5q5wBkRO4x7j9Bwnm4mUt1WliAwwSzgp8AsPwfXLAZ2"

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code
        self.disconnect()

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.sample()
