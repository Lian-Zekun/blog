from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

from blog.models import Article


# 博文的评论
class Comment(MPTTModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='art_comments', verbose_name=_('文章'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name=_('评论用户'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    reply_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='replyers', verbose_name=_('被评论用户'))
    content = RichTextField(verbose_name=_('评论内容'))
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name=_('发布日期'))

    class MPTTMeta:
        order_insertion_by = ['-publish_time']

    def __str__(self):
        return self.content[:20]
