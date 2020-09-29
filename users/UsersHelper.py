from likes.models import Like
from posts.serializers import PostSerializer

def set_like_status(post, profile):
    is_liked = "false"
    if Like.objects.filter(post=post, profile=profile).exists():
        is_liked = "true"
    return {"post": PostSerializer(post).data, "is_liked": is_liked, "like_count": post.post_likes.count()}
