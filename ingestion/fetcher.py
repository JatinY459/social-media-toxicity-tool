from .reddit_client import get_reddit_client

def fetch_posts(subreddit_name, limit=100):
    """
    Fetches the latest 'limit' posts from a given subreddit.
    Returns a list of dictionaries with post metadata.
    """
    reddit = get_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for submission in subreddit.new(limit=limit):
        posts.append({
            "id": submission.id,
            "title": submission.title,
            "selftext": submission.selftext,
            "created_utc": submission.created_utc,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "url": submission.url,
            "author": str(submission.author),
            "subreddit": str(subreddit)
        })
    return posts

def fetch_comments(post_id, limit=50):
    """
    Fetches comments for a specified post ID.
    Returns a list of dictionaries with comment data.
    """
    reddit = get_reddit_client()
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)  # flatten comment tree
    comments = []
    for comment in submission.comments.list()[:limit]:
        comments.append({
            "comment_id": comment.id,
            "body": comment.body,
            "created_utc": comment.created_utc,
            "score": comment.score,
            "author": str(comment.author),
            "post_id": post_id
        })
    return comments
