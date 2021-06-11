################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib

################################################################

async def speedtest(ctx):
    test_speed = lambda: utils.speedtest()
    ping, download, upload = await ctx.async_exec(test_speed)
    ping = str(round(ping))
    download = str(round(download, 2))
    upload = str(round(upload, 2))
    text = f"Ping: `{ping} ms`\nDownload: `{download} Mbits/s`\
    \nUpload: `{upload} Mbits/s`"
    title = loclib.Loc.member("label_internet_speed", ctx.author)
    embed = cembed.get_cembed(ctx.msg, text, title)
    await ctx.reply(embed=embed)

################################################################
