![alt text](http://pluralconcepts.com/images/quotebot.jpg "Quotebot")
<h1>QUOTEBOT</h1>

Quotebot is a Slack Bot providing stock quotes (15 min delay) and fast auto-complete company searches from Google Finance.

Installation
------------

   1. Make sure you have python installed on your laptop. (https://www.python.org/downloads/)
   2. Git clone this repo into your local folder
   3. cd into the quotebot folder
   4. Install the python modules required: pip install -r requirements.txt
   5. Create a new slack app, named "quotebot" for your slack team (for complete instructions, https://api.slack.com/slack-apps)
        *Go to https://api.slack.com/apps and click on Create New App
        *Enter quotebot for the app name.
	*Take note of the value in Client ID and set the environment variable:  SLACK_CLIENT_ID, e.g. export SLACK_CLIENT_ID=738473984.482347872
	*Take note of the value in Client Secret and set the environment variable: SLACK_CLIENT_SECRET, e.g. export SLACK_CLIENT_SECRET=8748fh93jd
	*Take note of the value in Verification Token and set the environment variable: SLACK_VERIFICATION_TOKEN, e.g. export SLACK_VERIFICATION_TOKEN=sh3hdbsu77u7
   6. In the left pane under Features, click on Incoming Webhooks and click on Enable Incoming Webhooks	
   7. In the left pane under Features, click on Bot Users and then Add Bot User using "quotebot" as the default user name. Click Always Show My Bot as Online.
   8. Start your server: python app.py
   9. The server listens on the default port: 4390
   10. In order for the next steps to work - you will need to expose this port - you could use ngrok to do this (see https://ngrok.com)
   11. In the left pane under Features, click on Event Subscriptions and Enable Events
        a. In the Enable Events Request URL: enter the event listener endpoint of this flask application, e.g. http://44f802c9.ngrok.io
        b. Add the following Team Events:  message.channels, message.im, pin_added, reaction_added, team_join
	c. Click Save Changes
   12. In the left pane under Features, click on Interactive Messages
        a. In Request URL, enter the endpoint for the option selection listener: .../actions e.g. http://44f802c9.ngrok.io/actions
	b. In the Options Load URL, enter the endpoint for the message menu listener: .../options e.g. http://44f802c9.ngrok.io/options
	c. Click on Enable Interactive Messages
   13. In the left pane under Settings, click on Install App. This will generate the tokens you'll need to interact with the Slack API
        a. Click on Permissions
        b. Add the following Redirect URL endpoint which references the oauth endpoint in this server: .../oauth e.g, http://44f802c9.ngrok.io/oauth
	c. Take note of the value of OAuth Access Token, and set the environment variable SLACK_BOT_TOKEN with this value .g. export SLACK_BOT_TOKEN=xoxb-193692833939-O5btIpdfjbTNFLocOxh7aThas
   14. Set up the bot:
        a. Stop the server by entering Ctrl-C
        b. Set the environment variable SLACK_BOT_NAME to "quotebot". e.g. export SLACK_BOT_NAME=quotebot
        c. run: python print_bot_id.py
	d. Take note of the value of the Bot ID for 'quotebot'
	e. Set the environment variable SLACK_BOT_ID to the value noted above.
   15. At this point you should have the following environment variables set correctly (would be good to put them in your login profile):
        SLACK_CLIENT_ID
        SLACK_CLIENT_SECRET
        SLACK_VERIFICATION_TOKEN
        SLACK_BOT_NAME
        SLACK_BOT_ID
        SLACK_BOT_TOKEN
   16. Start your server: python app.py
   17. Go to your slack client app and invite @quotebot to your channel.
   18. Type: @quotebot hello
   19. You should see:  Hello! Do you need a stock quote? For example type: q amzn

Design
------

Quotebot is a server using Python Flask and integrates with:

    1. Slack Events frameork (https://api.slack.com/events)
    2. Slack Message Menus framework (https://api.slack.com/docs/message-menus)
    3. Google Finance API (https://www.google.com/finance)

The Quotebot server implements 3 essential listeners or REST endpoints:

    1. Slack message event listener - listens for messages directed to our bot
    2. Slack message menu listener  - constructs a list of menu options to be shown to the user
    3. Slack menu option selected listener - takes action when the user selects a menu option

The following diagram shows the flow of events from the time a user asks for a quote to when the quote is displayed on the user's slack channel.

![alt text](http://pluralconcepts.com/images/quotebot-design.jpg "Quotebot Design")

   1. User types: @quotebot q int
   2. The event listener receives "q int", parses and looks up the symbol from its internal trie structures.
   3. It finds that there are several symbols starting with "int" - so it remembers the search string and posts back to Slack with a message menu attachment.
   4. Slack calls back to our message menu listener.
   5. The message listener responds with the list of companies which begin with the search string (limited to 15).
   6. The user sees a searchable message menu with the list of companies
   7. The user selects a company
   8. The option selection listener receives the company selected by the user
   9. It looks up the stock price from Google Finance and posts it back to Slack
   10. The user sees the price.

Note that in step 7, the user may not select a company but instead continues to type in the search box of the message menu.
If this happens, steps 4, 5 and 6 are repeated.

License
-------
Apache 2 License 2.0 (https://opensource.org/licenses/Apache-2.0)