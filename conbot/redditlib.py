### Imports

# Dependencies
import asyncpraw as praw

# Conbot Modules
import const

### Initialization

# Reddit Client
reddit = praw.Reddit(
    client_id=const.reddit_client_id,
    client_secret=const.reddit_secret,
    user_agent=const.reddit_user_agent,
)

### Function Definitions

# Get Posts
async def get_posts(
    subreddit: str,
    limit: int=10,
    sort_by: str="hot",
) -> list[praw.reddit.models.Submission]:
    """
    Gets posts from a subreddit.
    """
    try:
        subreddit = await reddit.subreddit(subreddit)
        submissions = getattr(subreddit, sort_by)
        posts = []
        async for post in submissions(limit=limit):
            posts.append(post)
        return posts
    except Exception as error:
        if error.__class__.__name__ != "NotFound": raise error

# Random Post
async def random_post(subreddit: str) -> praw.reddit.models.Submission:
    """
    Gets a random post from a subreddit.
    """
    try:
        subreddit = await reddit.subreddit(subreddit)
        return await subreddit.random()
    except Exception as error:
        if error.__class__.__name__ != "NotFound": raise error
