import socket

import requests


class InvalidTwitchAccountException(Exception):
    pass


class TwitchAccount:
    def __init__(self, twitch_config):
        self.twitch_config = twitch_config
        self.request_headers = {'Client-ID': self.twitch_config.get_client_id()}
        self.channel_api_url = 'https://api.twitch.tv/kraken/channels/'
        self.validate_twitch_account()

    def get_account_name(self):
        return self.twitch_config.get_account_name().lower()

    def get_secret_token(self):
        return self.twitch_config.get_client_secret()

    def validate_twitch_account(self):
        url = self.channel_api_url + self.twitch_config.get_account_name()
        response = requests.get(url=url, headers=self.request_headers)
        if not response.status_code == 200:
            print(response.content)
            raise InvalidTwitchAccountException('Twitch API returned following status code: {}'.format(response.status_code))


class TwitchChatBot:
    irc_host = 'irc.twitch.tv'
    irc_port = 6667
    buffer_size = 1024
    initial_buffer_size = 2 * buffer_size

    def __init__(self, channel_name, twitch_account, verbose=False):
        self.channel_name = channel_name
        self.connection = socket.socket()
        self.account = twitch_account
        self.verbose = verbose

    def log(self, log_string):
        if self.verbose:
            print('[TWITCH] {}'.format(log_string.strip()))

    def initialise_socket(self):
        self.connection = socket.socket()

    def connect(self):
        self.log('Opening socket')
        self.initialise_socket()
        self.connection.connect((self.irc_host, self.irc_port))

    def disconnect(self):
        self.log('Closing connection')
        self.connection.close()

    def join_channel(self):
        self.log('Joining channel')
        self.send('PASS oauth:{}'.format(self.account.get_secret_token()))
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

    def quick_post_in_channel(self, chat_string):
        self.connect()
        self.join_channel()
        self.receive()
        self.post_in_channel(chat_string=chat_string)
        self.disconnect()

    def post_in_channel(self, chat_string):
        self.send('PRIVMSG #{} :{}'.format(self.channel_name, chat_string))

    def send(self, send_string):
        send_string += '\r\n'
        self.log('Sending: {}'.format(send_string))
        self.connection.send(send_string.encode('utf-8'))


class CharityBot(TwitchChatBot):
    donation_string = 'A new donation of {}{} has been received!' \
                      ' A total of {}{} has been raised so far, thank you so much!'

    advert_strings = [
        '{} is being supported by Charitybot2, a twitch bot designed to supercharge charity streams. More info'
        'can be found here: TODO: INSERT URL'
    ]

    def __init__(self, channel_name, twitch_account, fundraiser_name, verbose=False):
        super().__init__(channel_name=channel_name, twitch_account=twitch_account, verbose=verbose)
        self.fundraiser_name = fundraiser_name
        self.current_advert_index = 0

    def post_donation_to_chat(self, donation_currency, donation_amount, total_raised):
        self.quick_post_in_channel(
            self.donation_string.format(
                donation_currency,
                donation_amount,
                donation_currency,
                total_raised))

    def post_advert_to_chat(self):
        self.quick_post_in_channel(chat_string=self.advert_strings[self.current_advert_index])
        self.current_advert_index += 1
        if self.current_advert_index >= len(self.advert_strings):
            self.current_advert_index = 0
