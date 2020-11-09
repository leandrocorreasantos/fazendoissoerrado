from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Category, Post


# Create your views here.


def index(request):
    posts = Post.objects.filter(
        published=True
    ).all()[:10]

    return render(
        request,
        'blog/index.html',
        {'posts': posts}
    )
