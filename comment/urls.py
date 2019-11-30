from django.urls import path

from . import views

app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>', views.comments_view, name='post_comment'),
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.comments_view, name='reply_comment'),
    path('delete-comment/<int:article_id>/<int:comment_id>', views.delete, name='delete_comment')
]
