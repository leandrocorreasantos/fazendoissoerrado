from django import template
from django.utils import timezone
from adsense.models import Banner

register = template.Library()


@register.inclusion_tag('templatetags/adsense.html')
def show_ads(size='0x0'):
    sizes = size.split('x')
    width = sizes[0]
    height = sizes[1]

    queryset = Banner.objects.filter(
        size__width__in=["0", width]
    ).filter(
        size__height__in=["0", height]
    ).filter(
        start_campaign__lte=timezone.now()
    ).filter(
        end_campaign__gte=timezone.now()
    ).filter(active=True).order_by('?')

    ads = queryset.first()

    return {'ads': ads, 'width': width, 'height': height}
