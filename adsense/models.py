import os
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.


class SizeBanner(models.Model):
    name = models.CharField(max_length=60)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return "{}x{}".format(self.width, self.height)


class Banner(models.Model):
    size = models.ForeignKey(SizeBanner, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='adsense/', blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    start_campaign = models.DateTimeField(default=timezone.now)
    end_campaign = models.DateTimeField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self):
        if self.pk:
            this = Banner.objects.get(pk=self.pk)
            try:
                if this.image != self.image:
                    if os.path.isfile(this.image.path):
                        os.remove(this.image.path)
            except Exception:
                pass

        super(Banner, self).save()


@receiver(pre_delete, sender=Banner)
def delete_image(sender, instance, *args, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
