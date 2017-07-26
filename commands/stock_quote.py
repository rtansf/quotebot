from .command import Command
import requests
import json

class StockQuote(Command):

    def execute(self):
        symbol_or_name = self.params['selected']
        company_trie = self.params['company-trie']
        symbol_trie = self.params['symbol-trie']
        val = company_trie.get(symbol_or_name)
        symbol = None
        if val is not None:
            symbol = val
        else:
            val = symbol_trie.get(symbol_or_name)
            if val is not None:
                symbol = symbol_or_name

        #print ('looking up symbol for ' + symbol)
        cname = symbol_trie.get(symbol)
        if symbol is None:
            return 'Unable to get stock quote for: ' + symbol_or_name
        else:
            r = requests.get('http://finance.google.com/finance/info?q=' + symbol)
            #print (r.text)
            payload = r.text[3:]
            j = json.loads(payload)
            delta_string = j[0]['c']
            delta = float(delta_string)
            direction = ''
            if delta < 0:
                direction = ':arrow_down:'
            elif delta > 0:
                direction = ':arrow_up:'
            return cname + ' (' + symbol + ') : ' + j[0]['l'] + '  ' + direction + ' ' + delta_string
