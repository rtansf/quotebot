'''

   QUOTEBOT

   A workbot offering autocomplete company search and gives stock quotes via Slack

   Author:  Rob Tan  (rtansf@gmail.com)
   Date Created:  06-15-2017
   
   Software License: Apache License 2.0 (https://opensource.org/licenses/Apache-2.0)

'''
from flask import Flask
from flask import request, jsonify, make_response
from bot_exception import BotException
from slackclient import SlackClient
from config import Config
from bot import Bot
import requests
import json

config = Config()
slack_client = SlackClient(config.bot_token)
bot = Bot()

app = Flask(__name__)

@app.errorhandler(BotException)
def handle_bot_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#
# Message Event Listener
# Entry point for all events from slack
#
@app.route('/quotebot', methods=['POST','GET'])
def event_listener():

    print ('in event_listener')
    print (request.data)
    print ('-----------------')

    request.data = str(request.data, 'utf-8')
    
    slack_event = json.loads(request.data)
    print ('slack_event = ')
    print (slack_event)
    print ('------------------')
    
    token = slack_event['token']

    if token != config.verification_token:
        raise BotException('Invalid verification token received. Access forbidden', status_code=410)

    if 'challenge' in slack_event:
        challenge = slack_event['challenge']
        return jsonify ({"challenge" : challenge})

    if 'event' in slack_event:
        message = bot.handle_event(slack_event)
        return make_response(message, 200)

    return make_response('', 200)

#
# OAUTH
#
@app.route('/quotebot/oauth', methods=['POST','GET'])
def oauth():
    code = request.args.get('code')
    if code == None:
        raise BotException('We are not getting a code', status_code=500)

    qs = { 'code': code, 'client_id': config.client_id, 'client_secret': config.client_secret }
    r = requests.get('https://slack.com/api/oauth.access', params=qs, timeout=10)
    return r.text

#
# Message Menu Listener
#
@app.route('/quotebot/options', methods=["POST"])
def menu_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    print ('in menu_options')
    print (form_json)
    print ('---------------')

    menu_options = bot.get_menu_options(form_json)
    return jsonify(menu_options)

#
# Option Selection Listener
#
@app.route('/quotebot/actions', methods=['POST'])
def actions():
    payload = json.loads(request.form['payload'])
    
    print('in actions')
    print(payload)
    print('----------')

    resp = bot.handle_option_selected(payload)
    return jsonify(resp)


#
# Ping
#
@app.route('/quotebot/ping', methods=['POST','GET'])
def ping():
    return 'I\'m alive'

if __name__ == '__main__':
    app.run(host='0.0.0.0')

