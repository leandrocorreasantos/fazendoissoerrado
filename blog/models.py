import os
import glob
from slugify import slugify
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from taggit.managers import TaggableManager
from tinymce.models import HTMLField
# Create your models here.


class Category(models.Model):
    name = models.CharField('Nome', max_length=255)
    slug = models.CharField('Slug', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/category/{}".format(self.slug)

    def save(self):
        self.slug = slugify(self.name)
        super(Category, self).save()


class Post(models.Model):
    title = models.CharField('Título', max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT
    )
    slug = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField('Conteúdo', blank=True, null=True)
    meta_description = models.TextField('meta-escription')
    cover = models.ImageField(
        'Capa', upload_to='post/cover/', blank=True, null=True
    )
    published = models.BooleanField('Publicado', default=False)
    created_date = models.DateTimeField('Criado em', default=timezone.now)
    published_date = models.DateTimeField(
        'Publicado em',
        blank=True,
        null=True
    )
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/{}-{}".format(self.category, self.slug)

    def publish(self):
        self.published_date = timezone.now()
        self.published = True
        self.save()

    def save_as_draft(self):
        self.published_date = None
        self.published = False
        self.save()

    def save(self):
        if self.pk:
            slug_field = '{}-{}-{}'.format(
                self.category, self.title, self.pk
            )
            self.slug = slugify(slug_field)

            this = Post.objects.get(pk=self.pk)
            try:
                if this.cover != self.cover:
                    path = "%s*" % (this.cover.path)
                    for arq in glob.glob(path):
                        os.remove(arq)
            except Exception:
                pass

        super(Post, self).save()


@receiver(pre_delete, sender=Post)
def delete_cover(sender, instance, *args, **kwargs):
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)
