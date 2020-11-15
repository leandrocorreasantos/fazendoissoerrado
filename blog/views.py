from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Post
from django.shortcuts import get_object_or_404
from django.utils import timezone


# Create your views here.


def post_details(request, category, slug, pk):
    queryset = Post.objects.filter(
        published=True
    ).filter(
        published_date__lt=timezone.now()
    ).filter(pk=pk)
    post = get_object_or_404(queryset)
    keywords = post.taglist()
    ''' prevent counter view to repeat counter on update page '''
    last_post = request.session.get('LAST_POST', None)
    this_post = request.path
    if not last_post or this_post != last_post:
        ''' increment counter from post '''
        post.views += 1
        post.save()
        ''' remember the last post viewed '''
        request.session['LAST_POST'] = this_post

    return render(
        request,
        'blog/post_details.html',
        {'post': post, 'keywords': keywords}
    )


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
    post_search = Post.objects.filter(
        published_date__lte=timezone.now()
    ).filter(published=True).filter(
        tags__name__in=[tag_name]
    ).order_by('-published_date').all()

    if not post_search:
        return render(
            request,
            'blog/list_by_tag.html'
        )

    paginator = Paginator(post_search, 10)
    posts = paginator.get_page(page)

    return render(
        request,
        'blog/list_by_tag.html',
        {'posts': posts}
    )
