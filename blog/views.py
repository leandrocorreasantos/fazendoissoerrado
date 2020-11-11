from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Category, Post
from django.utils import timezone


# Create your views here.


def index(request):
    page = request.GET.get('page', 1)
    highlights = Post.find()[:3]
    post_search = Post.find()
    paginator = Paginator(post_search, 5)
    posts = paginator.get_page(page)

    return render(
        request,
        'blog/index.html',
        {'posts': posts, 'highlights': highlights}
    )
