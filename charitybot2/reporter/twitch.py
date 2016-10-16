import socket
import requests

class InvalidTwitchAccountException(Exception):
    pass


class TwitchAccount:
    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.request_headers = {'Client-ID': self.token}
        self.channel_api_url = 'https://api.twitch.tv/kraken/channels/'
        self.validate_twitch_account()

    def get_account_name(self):
        return self.name

    def get_secret_token(self):
        return self.token

    def validate_twitch_account(self):
        url = self.channel_api_url + self.name
        response = requests.get(url=url, headers=self.request_headers)
        if not response.status_code == 200:
            raise InvalidTwitchAccountException('Twitch API returned following status code: {}'.format(response.status_code))


class TwitchChat:
    irc_host = 'irc.twitch.tv'
    irc_port = 6667
    buffer_size = 1024
    initial_buffer_size = 4 * buffer_size

    def __init__(self, channel_name, twitch_account, verbose=False):
        self.channel_name = channel_name
        self.connection = socket.socket()
        self.account = twitch_account
        self.verbose = verbose

    def log(self, log_string):
        if self.verbose:
            print('[TWITCH] {}'.format(log_string))

    def connect(self):
        self.log('Opening connection')
        self.connection.connect((self.irc_host, self.irc_port))

    def disconnect(self):
        self.log('Closing connection')
        self.connection.close()

    def join_channel(self):
        self.send('PASS {}'.format(self.account.get_secret_token()))
        self.send('NICK {}'.format(self.account.get_account_name()))
        self.send('USER {}'.format(self.account.get_account_name()))

    def receive(self):
        self.log('Checking for data')
        response = self.connection.recv(self.buffer_size)
        return self.check_for_ping(response)

    def check_for_ping(self, data):
        data = data.decode('utf-8')
        if data == 'PING :tmi.twitch.tv\r\n':
            self.send('PONG :tmi.twitch.tv')
            self.log('Responded to PING with PONG')
            return ''
        self.log('Recived data: {}'.format(data))
        return data

    def post_in_channel(self, chat_string):
        self.connect()
        self.send('PRIVMSG {}:{}'.format(self.channel_name, chat_string))
        self.disconnect()

    def send(self, send_string):
        send_string += '\\r\\n'
        self.log('Sending: {}'.format(send_string))
        self.connection.send(send_string.encode('utf-8'))
