### Imports

# Standard Library
from typing import Callable

# Dependencies
import discord

### Class Definitions

# Bot
class Bot(discord.Client):
    """
    Represents a Discord bot.
    """

    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.global_vars = {}

    async def async_exec(self, func: Callable):
        """
        Executes a function asynchronously.
        """
        return await self.loop.run_in_executor(None, func)
