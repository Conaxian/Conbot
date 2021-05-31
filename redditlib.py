################################################################

import asyncpraw as praw

import const

################################################################

reddit = praw.Reddit(
    client_id=const.reddit_client_id,
    client_secret=const.reddit_secret,
    user_agent=const.reddit_user_agent,
)

################################################################

# Get posts from a subreddit

async def get_posts(subreddit, limit=10, sort_by="hot"):

    subreddit_ = await reddit.subreddit(subreddit)
    submissions = getattr(subreddit_, sort_by)
    posts = []
    async for post in submissions(limit=limit):
        posts.append(post)
    return posts

################################################################

# Get a random post from a subreddit

async def random_post(subreddit):

    subreddit_ = await reddit.subreddit(subreddit)
    post = await subreddit_.random()
    return post

################################################################
