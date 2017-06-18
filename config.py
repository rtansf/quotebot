import os

class Config():

    def __init__(self):

        self.client_id = os.environ.get('SLACK_CLIENT_ID')
        self.client_secret = os.environ.get('SLACK_CLIENT_SECRET')
        self.verification_token = os.environ.get('SLACK_VERIFICATION_TOKEN')
        self.bot_id = os.environ.get('SLACK_BOT_ID')
        self.bot_token = os.environ.get('SLACK_BOT_TOKEN')


