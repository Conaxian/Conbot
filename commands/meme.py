################################################################

import sys
import random

sys.path.append("..")

import const
import cembed
import redditlib

################################################################

async def meme(ctx):

    subreddit = random.choice(const.meme_subreddits)
    post = await redditlib.random_post(subreddit)
    permalink = f"https://www.reddit.com{post.permalink}"
    embed = cembed.get_cembed(ctx.msg, title=post.title, 
    url=permalink, image=post.url, footer=f"r/{subreddit}")
    await ctx.reply(embed=embed)

################################################################
