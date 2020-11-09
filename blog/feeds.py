from django.contrib.syndication.views import Feed
from .models import Post


class LatestEntriesFeed(Feed):
    title = "Fazendo Isso Errado - Novidades"
    link = "/feed/"
    description = "Tudo que pintou de novo no blog"

    def items(self):
        return Post.objects.filter(
            published=True
        ).order_by('-published_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.meta_description

