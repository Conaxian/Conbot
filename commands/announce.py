################################################################

import sys

sys.path.append("..")

################################################################

async def announce(ctx):

    parts = ctx.args["channel, message"].split(" ")
    message = ctx.args["channel, message"][len(parts[0]):]
    channel_id = int(parts[0])
    channel = await ctx.client.fetch_channel(channel_id)
    await channel.send(message.strip())

################################################################
