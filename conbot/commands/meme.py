### Imports

# Standard Library
import sys
from random import choice

# Conbot Modules
sys.path.append("..")
import const
from cembed import cembed
from redditlib import random_post

### Command

# Command Meta
meta = {
    "name": "meme",
    "aliases": [
        "memes",
    ],
    "category": "images",
    "index": 0,
}

# Command Call
async def call(ctx):
    subreddit = choice(const.meme_subreddits)
    post = await random_post(subreddit)
    permalink = "https://www.reddit.com" + post.permalink
    embed = cembed(ctx, title=post.title, url=permalink, 
        image=post.url, footer="r/" + subreddit, footer_icon=" ")
    await ctx.reply(embed=embed)
