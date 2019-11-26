import asyncio

class Command(object):
    # Represents an individual command type.
    def __init__(self, handler, helpstr):
        self.handler=handler
        self.help=helpstr

    @asyncio.coroutine
    def call(self, cmdList):
        pass

class Bot(object):
    def __init__(self, client, prefix='~'):
        self.cmddict = {}
        self.client = client
        self.prefix = prefix

    def add_command(self, name, cmd):
        self.cmddict[name]=cmd

    @asyncio.coroutine
    def comprehend(self, message):
        content = message.content
        if !content.startswith(self.prefix):
            return
        parsed = content[len(self.prefix):].split(' ')
        cmd = parsed.pop(0)
        if cmd in self.cmddict:
            yield from self.client.send_message(message.channel, self.cmddict[cmd].call(parsed))
        else:
            yield from self.client.send_message(message.channel, "Unknown command: '%s'" % cmd)
