import pygtrie
import requests
import os
import csv
from slackclient import SlackClient
from commands.stock_quote import StockQuote
from commands.hello import Hello

from controls import Controls
from config import Config

class Bot():

    company_trie = None
    symbol_trie = None
    user_commands = {}

    def __init__(self):
        self.config = Config()
        self.slack_client = SlackClient(self.config.bot_token)

        # Create tries if necessary
        # This is used for auto-complete
        if Bot.company_trie is None:
            Bot.company_trie = pygtrie.CharTrie()
            Bot.symbol_trie = pygtrie.CharTrie()
            full_path = os.path.realpath(__file__)
            path = os.path.dirname(full_path)
            with open(path + '/resources/nasdaq.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cname = row['Name'].strip().upper()
                    symbol = row['Symbol'].strip().upper()
                    Bot.company_trie[cname] = symbol
                    Bot.symbol_trie[symbol] = cname

            with open(path + '/resources/nyse.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cname = row['Name'].strip().upper()
                    symbol = row['Symbol'].strip().upper()
                    Bot.company_trie[cname] = symbol
                    Bot.symbol_trie[symbol] = cname


    def get_menu_options(self, form_json):

        name = form_json['name'].upper()
        value = form_json['value'].upper()
        callback_id = form_json['callback_id']
        user = form_json['user']['id']

        print ('in get_menu_options')
        print ('name = ' + name + ' value = ' + value + ' callack_id = ' + callback_id + ' user = ' + user)
        print ('-------------------')


        given_prefix = form_json['name'].upper()
        options = []
        if value == '':
            prefix = given_prefix
        else:
            prefix = value

        menu_options = { "options": options }

        trie = None
        if callback_id == 'company_name_options':
            trie = Bot.company_trie

        try:
            items = trie.items(prefix=prefix)
            maxnum = len(items)
            if maxnum > 15:
                maxnum = 15
            for i in range(0, maxnum):
                cname = items[i][0]
                sym = Bot.company_trie.get(cname)
                option_value = cname + ' (' + sym + ') '
                options.append({"text": option_value, "value": sym})
        except:
            pass

        return menu_options

    def handle_option_selected(self, payload):

        user = payload['user']
        user_name = user['name']
        user_id = user['id']
        channel = payload['channel']['id']
        action_name = payload['actions'][0]['name']
        type = payload['actions'][0]['type']
        option = payload['actions'][0]['selected_options'][0]['value']

        print ('in handle_option_selected')
        print ('user = ' + user_id + ' channel = ' + channel + ' name = ' + action_name + ' type = ' + type + ' option = ' + option)
        print ('-------------------------')

        resp_text = 'selected: ' + option
        key = channel+user_id
        if key in Bot.user_commands:
            user_command = Bot.user_commands[key]
            user_command.set_param('selected', option)
            resp_text = user_command.execute()

        resp = {}
        resp['text'] = resp_text
        resp['replace_original'] = True
        return resp

    def handle_event(self, slack_event):
        event = slack_event['event']
        event_type = event['type']
        if 'user' not in event:
            return 'OK'

        user = event['user']
        if user == self.config.bot_id:
            return 'OK'  # Dont do anything about own messages

        channel = event['channel']

        if 'text' in event:
            text = event['text']
            print('in handle_event')
            print('event_type = ' + event_type + ' channel = ' + channel + ' user = ' + user + ' text = ' + text)
            print('---------------')

            # Reply to request
            AT_BOT = '<@' + self.config.bot_id + '>'

            command = text
            if  True:
                if text.startswith(AT_BOT):
                    command = text.split(AT_BOT)[1].strip().lower()

                if command.startswith('quote') or command.startswith('q ') or command.startswith('Q ') or command.startswith('Quote'):
                    toks = command.split(' ')
                    sym_or_name = toks[1].upper()
                    user_command = StockQuote(name="stock_quote", intent="get_stock_quote", params={}, raw=command,
                                             urls={})
                    user_command.set_param('company-trie', Bot.company_trie)
                    user_command.set_param('symbol-trie', Bot.symbol_trie)
                    user_command.set_param('selected', sym_or_name)

                    val = Bot.symbol_trie.get(sym_or_name)
                    if val is not None:
                        self.postToSlack(channel, user_command.execute(), {})
                    else:
                        controls = Controls()
                        Bot.user_commands[channel+user] = user_command
                        controls.message_attachments_company_name_options[0]['actions'][0]['name'] = sym_or_name
                        message = 'Hmm, I don\'t know that stock symbol.\n Please use the search box below'
                        self.postToSlack(channel, message, controls.message_attachments_company_name_options)

                else:
                    # Fallback to saying hello!
                    user_command = Hello(name="hello", intent="say_hello", params={}, raw=command, urls={})
                    self.postToSlack(channel, user_command.execute(), {})

        return 'OK'

    def postToSlack(self, channel, message, attachments):
        self.slack_client.api_call("chat.postMessage", channel=channel,
                                   text=message, as_user=True, attachments=attachments)
