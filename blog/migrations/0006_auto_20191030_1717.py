# Generated by Django 2.2.1 on 2019-10-30 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20191030_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='html_content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='toc',
            field=models.TextField(blank=True),
        ),
    ]
