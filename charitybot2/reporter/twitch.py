import socket
import requests


class InvalidTwitchAccountException(Exception):
    pass


class TwitchAccount:
    def __init__(self, name, client_id, client_secret):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.request_headers = {'Client-ID': self.client_id}
        self.channel_api_url = 'https://api.twitch.tv/kraken/channels/'
        self.validate_twitch_account()

    def get_account_name(self):
        return self.name

    def get_secret_token(self):
        if 'oauth:' not in self.client_secret:
            return 'oauth:' + self.client_secret
        return self.client_secret

    def validate_twitch_account(self):
        url = self.channel_api_url + self.name
        response = requests.get(url=url, headers=self.request_headers)
        if not response.status_code == 200:
            print(response.content)
            raise InvalidTwitchAccountException('Twitch API returned following status code: {}'.format(response.status_code))


class TwitchChatBot:
    irc_host = 'irc.twitch.tv'
    irc_port = 6667
    buffer_size = 1024
    initial_buffer_size = 1 * buffer_size

    def __init__(self, channel_name, twitch_account, verbose=False):
        self.channel_name = channel_name
        self.connection = socket.socket()
        self.account = twitch_account
        self.verbose = verbose

    def log(self, log_string):
        if self.verbose:
            print('[TWITCH] {}'.format(log_string.strip()))

    def connect(self):
        self.log('Opening socket')
        self.connection.connect((self.irc_host, self.irc_port))

    def disconnect(self):
        self.log('Closing connection')
        self.connection.close()

    def join_channel(self):
        self.log('Joining channel')
        self.send('PASS {}'.format(self.account.get_secret_token()))
        self.send('NICK {}'.format(self.account.get_account_name()))
        self.send('USER {}'.format(self.account.get_account_name()))
        self.send('JOIN {}'.format(self.channel_name))

    def receive(self):
        self.log('Checking for data')
        response = self.connection.recv(self.buffer_size)
        return self.check_for_ping(response)

    def check_for_ping(self, data):
        data = data.decode('utf-8')
        if data == 'PING :tmi.twitch.tv\r\n':
            self.send('PONG :tmi.twitch.tv\r\n')
            self.log('Responded to PING with PONG')
            return ''
        self.log('Received data: {}'.format(data))
        return data

    def post_in_channel(self, chat_string):
        self.connect()
        self.join_channel()
        self.receive()
        self.send('PRIVMSG #{} :{}'.format(self.channel_name, chat_string))
        self.disconnect()

    def send(self, send_string):
        send_string += '\r\n'
        self.log('Sending: {}'.format(send_string))
        self.connection.send(send_string.encode('utf-8'))
