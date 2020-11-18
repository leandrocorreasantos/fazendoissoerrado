from django.contrib import admin
from .models import Banner, SizeBanner
# Register your models here.


class SizeBannerAdmin(admin.ModelAdmin):
    list_display = ['name', 'width', 'height']


class BannerAdmin(admin.ModelAdmin):
    list_filter = ['size', 'title']


admin.site.register(SizeBanner, SizeBannerAdmin)
admin.site.register(Banner, BannerAdmin)
