from django import template
from django.utils import timezone
from blog.models import Post

register = template.Library()


@register.inclusion_tag('templatetags/post_list.html')
def most_viewed():
    title = 'Mais Vistos'
    posts = Post.objects.filter(
        published_date__lt=timezone.now()
    ).filter(
        published=True
    ).order_by('-views').all()[:5]
    return {'posts': posts, 'title': title}


@register.inclusion_tag('templatetags/post_list.html')
def most_recent():
    title = 'Mais Recentes'
    posts = Post.objects.filter(
        published_date__lt=timezone.now()
    ).filter(published=True).order_by('-published_date').all()[:5]
    return {'posts': posts, 'title': title}


@register.inclusion_tag('templatetags/post_list_footer.html')
def most_recent_footer():
    posts = Post.objects.filter(
        published_date__lt=timezone.now()
    ).filter(published=True).order_by('-published_date').all()[:5]
    return {'posts': posts}
