# Generated by Django 2.2 on 2020-11-08 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Conteúdo'),
        ),
    ]
