class Command():

    def __init__(self, name, intent, params, raw, urls):
        self.name = name
        self.intent = intent
        self.params = params
        self.raw = raw
        self.urls = urls

    def set_param(self, name, value):
        self.params[name] = value

    def execute(self):
        return "Result of command execution"
