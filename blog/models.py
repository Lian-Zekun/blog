import re

from django.db import models
from django.utils.html import strip_tags
from mdeditor.fields import MDTextField  # Markdown字段
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

import markdown
from markdown.extensions.toc import TocExtension


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('分类名称'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', args=[self.id])

    class Meta:
        verbose_name = _('博客分类')
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('标签名称'))
    article_count = models.PositiveIntegerField(default=0, verbose_name=_('文章数'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', args=[self.id])

    class Meta:
        verbose_name = _('标签名称')
        verbose_name_plural = verbose_name
        unique_together = ("name",)


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('标题'))
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, verbose_name=_('类别名称'))
    tags = models.ManyToManyField(to='Tag', related_name='tags', blank=True, verbose_name=_("标签"))
    content = MDTextField(_('内容'))
    html_content = models.TextField(blank=True, editable=False)
    excerpt = models.CharField(max_length=200, editable=False, blank=True)  # 摘要
    toc = models.TextField(blank=True, editable=False)  # 文章目录
    pic = models.ImageField(verbose_name=_('博客封面图片'), upload_to='blog_pic/%Y%m%d/',
                            default='blog_pic/book.jpg', blank=True)
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name=_('发布日期'))
    modified_time = models.DateTimeField(auto_now=True, verbose_name=_('更改日期'))
    read_num = models.PositiveIntegerField(default=0, verbose_name=_('浏览数'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article', args=[self.id])

    def save(self, *args, **kwargs):
        if not kwargs.get('update_fields'):
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
            ])
            self.html_content = md.convert(self.content)  # 将文章内容渲染为html格式
            # 匹配目录是否有值的正则表达式
            directory = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
            self.toc = directory.group(1) if directory is not None else False  # 目录
            self.excerpt = strip_tags(self.html_content)[:90]
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-publish_time']
        verbose_name = _('文章')
        verbose_name_plural = verbose_name
