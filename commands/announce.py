################################################################

import sys

sys.path.append("..")

################################################################

async def announce(ctx):

    parts = ctx.args["channel, message"].split(" ")
    channel_id = int(parts[0])
    message = ctx.args["channel, message"][len(parts[0]):]
    for guild in ctx.client.guilds:
        for channel in guild.text_channels:
            if channel_id == channel.id:
                await channel.send(message.strip())

################################################################