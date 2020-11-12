from django.urls import path
from . import views
from .feeds import LatestEntriesFeed
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from .models import Post, Category


app_name = 'blog'

infodict_posts = {
    'queryset': Post.objects.filter(
        published=True
    ).order_by('-published_date'),
    'date_field': 'published_date'
}
infodicts_categories = {
    'queryset': Category.objects.order_by('name'),
    'date_field': None
}


class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority = '0.8'

    def items(self):
        return ['/']

    def location(self, item):
        return item


sitemaps = {
    'static': StaticSitemap,
    'posts': GenericSitemap(
        infodict_posts,
        priority=0.7, changefreq='weekly'
    ),
    'categories': GenericSitemap(
        infodicts_categories,
        priority=0.5, changefreq='monthly')
}

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='posts'),
    path('feed/', LatestEntriesFeed()),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path(
        'sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps},
        name='sitemaps'
    )
]
