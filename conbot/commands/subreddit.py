### Imports

# Standard Library
import sys
from random import choice

# Conbot Modules
sys.path.append("..")
import const
from utils import escape_md
from cmdtools import Arg, CmdError
from cembed import cembed
from redditlib import random_post

### Command

# Command Meta
meta = {
    "name": "subreddit",
    "aliases": [
        "post",
    ],
    "category": "images",
    "index": 0,
    "args": [
        Arg("<subreddit>", "word"),
    ],
}

# Command Call
async def call(ctx):
    subreddit = ctx.args["subreddit"]
    post = await random_post(subreddit)

    if not post:
        raise CmdError("cmd/subreddit/not_found")

    if post.over_18 and not ctx.channel.is_nsfw():
        raise CmdError("cmd/subreddit/nsfw")

    permalink = "https://www.reddit.com" + post.permalink
    embed = cembed(ctx,
        title=escape_md(post.title),
        url=permalink,
        image=post.url,
        footer="r/" + subreddit,
        footer_icon=" ",
    )
    await ctx.reply(embed=embed)
