# Generated by Django 2.2 on 2020-11-18 05:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SizeBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='adsense/')),
                ('code', models.TextField(blank=True, null=True)),
                ('start_campaign', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_campaign', models.DateTimeField()),
                ('active', models.BooleanField(default=False)),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adsense.SizeBanner')),
            ],
        ),
    ]
