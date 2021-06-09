################################################################

# Class for command context

class Context:

    def __init__(self, client, msg, prefix, args, commands, user_config, server_config, **kwargs):

        self.client = client
        self.msg = msg
        self.author = msg.author
        self.guild = msg.guild
        self.channel = msg.channel
        self.prefix = prefix
        self.args = args
        self.commands = commands
        self.user_config = user_config
        self.server_config = server_config
        self.global_vars = kwargs

    async def send(self, content=None, *args, tts=False, embed=None, file=None, files=None, 
    delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None):

        await self.channel.send(content, *args, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, 
        nonce=nonce, allowed_mentions=allowed_mentions, reference=reference, mention_author=mention_author)

    async def reply(self, content=None, *args, tts=False, embed=None, file=None, files=None, 
    delete_after=None, nonce=None, allowed_mentions=None):

        await self.channel.send(content, *args, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, 
        nonce=nonce, allowed_mentions=allowed_mentions, reference=self.msg, mention_author=False)

    async def async_exec(self, func):

        return await self.client.loop.run_in_executor(None, func)

################################################################

# Class for commands

class Command:

    def __init__(self, name, calls, category, args, delimiters, perms, desc, code, dev):

        self.name = name
        self.calls = calls
        self.category = category
        self.args = args
        self.delimiters = delimiters
        self.perms = perms
        self.desc = desc
        self.code = code
        self.dev = dev

    @classmethod
    def new(cls, name, aliases, category, args, delimiters, perms):

        aliases.append(name)
        desc = name.replace("-", "_")
        dev = True if category == "dev" else False
        return cls(name, aliases, category, args, delimiters, perms, desc, None, dev)

################################################################

# Command error (sends an error message)

class CmdError(Exception):
    pass

# Bot permission error (sends an error message)

class BotPermsError(Exception):
    pass

################################################################
