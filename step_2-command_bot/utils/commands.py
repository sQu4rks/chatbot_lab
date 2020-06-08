class Command:
    def __init__(self, keyword, callback):
        self.keyword = keyword
        self.callback = callback

    def get_keyword(self):
        return self.keyword

    def invoke(self, dnac, args):
        out_text = self.callback(dnac, args)

        return out_text

class CommandFactory:
    def __init__(self, dnac, msg_broker):
        self.commands = {}
        self.dnac = dnac
        self.msg_broker = msg_broker

    def create_command(self, keyword, callback):
        keyword = str(keyword).lower()
        c = Command(keyword, callback)
        self.commands[keyword] = c

    def get_command(self, keyword):
        keyword = str(keyword).lower()

        if keyword not in self.commands.keys():
            return None
        else:
            return self.commands[keyword]

    def run_command(self, keyword, args):
        keyword = str(keyword).lower()

        cmd = self.get_command(keyword)
        print("Command is {}".format(cmd))
        if cmd is not None:
            out = cmd.invoke(self.dnac, args)
            self.msg_broker.send(out)
