from .command import Command

class Hello(Command):

    def execute(self):
       return 'Hello! Do you need a stock quote? For example type: q amzn'