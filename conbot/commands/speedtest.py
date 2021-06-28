### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import utils
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "speedtest",
    "category": "tools",
    "index": 2,
}

# Command Call
async def call(ctx):
    speedtest = lambda: utils.speedtest()
    ping, download, upload = await ctx.bot.async_exec(speedtest)
    text = f"Ping: `{round(ping)} ms`\
        \n\
        Download: `{round(download, 2)} Mbits/s`\
        \n\
        Upload: `{round(upload, 2)} Mbits/s`"
    title = Loc("cmd/speedtest/title")
    embed = cembed(ctx, text, title=title)
    await ctx.reply(embed=embed)
