from django.core.cache import cache

from config.settings import CACHE_ENABLED
from blog.models import Post

def get_cached_posts():
    if CACHE_ENABLED:
        posts = cache.get('posts')
        if posts is None:
            posts = Post.objects.all()
            cache.set('posts', posts)
    else:
        posts = Post.objects.all()
    return posts