from django.shortcuts import render, get_object_or_404
import markdown
from .models import Post


# 主页
def index(request):
    context = Post.objects.all()
    return render(request, 'index.html', {'context': context})


# 文章详情页
def deta(request, blog_id):
    context = get_object_or_404(Post, pk=blog_id)
    config = {
        'codehilite': {
            'use_pygments': False,
            'css_class': 'prettyprint linenums',
        }
    }
    context.blog_body = markdown.markdown(context.blog_body, extensions=['codehilite'], extension_configs=config)
    return render(request, 'deta.html', {'context': context})
