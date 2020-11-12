from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Category, Post
from django.utils import timezone


# Create your views here.

def post_list(request):
    page = request.GET.get('page', 1)
    post_search = Post.find()
    paginator = Paginator(post_search, 10)
    posts = paginator.get_page(page)

    return render(
        request,
        'blog/post_list.html',
        {'posts': posts}
    )


def index(request):
    page = 1
    highlights = Post.find()[:3]
    post_search = Post.find()
    paginator = Paginator(post_search, 10)
    pagination = paginator.get_page(page)
    posts = pagination[3:]

    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
            'highlights': highlights,
            'pagination': pagination
        }
    )


def tag(request, tag_name):
    page = request.GET.get('page', 1)
    post_search = Post.find_by_tag(tag_name)
    paginator = Paginator(post_search, 10)
    posts = paginator.get_page(page)

    return render(
        request,
        'blog/list_by_tag.html',
        {'posts': posts}
    )
