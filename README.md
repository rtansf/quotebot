![alt text](http://pluralconcepts.com/images/quotebot.jpg "Quotebot")
<h1>QUOTEBOT</h1>

Quotebot is a Slack Bot providing stock quotes (15 min delay) and fast auto-complete company searches from Google Finance.

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

Installation
------------


License
-------