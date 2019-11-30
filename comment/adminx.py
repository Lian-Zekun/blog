import xadmin
from .models import Comment


class CommentAdmin(object):
    model_icon = 'fa fa-comments'  # 菜单图标


xadmin.site.register(Comment, CommentAdmin)
