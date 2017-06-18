from .command import Command

class Hello(Command):

    def execute(self):
       return 'Hello! How can I help you today?'