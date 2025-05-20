from django.db.models import Count
from langchain.tools import tool
from core.models import Post, Comment


@tool
def get_post_insights() -> str:
    """Fetch post contents and statistics (views, shares) for the marketing strategist."""
    posts = Post.objects.annotate(num_comments=Count('comments')).order_by(
        '-created_at')
    latest_posts = posts[:20]
    result = []

    for post in latest_posts:
        # I prefer this formatting "%H:%M:%S"
        created_time = post.created_at.strftime("%I:%M %p")

        views_count = post.views_count
        shared_count = post.shared_count
        comments_count = post.comments.count()
        engagement_value = (0.1 * views_count) + \
            (1.5 * shared_count) + (2 * comments_count)

        result.append(
            f"Post: {post.content} | Views: {views_count} | Shares: {shared_count} | "
            f"Comments: {comments_count} | Engagements: {engagement_value} | Created At: {created_time}"
        )

    latest_post_result = "\n".join(result)

    return (
        f"The company has {len(posts)} posts in total so far. The company has a total of {len(posts)} posts. "
        f"The latest posts are:\n{latest_post_result}"
    )
