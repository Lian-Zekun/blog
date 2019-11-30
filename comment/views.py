from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .forms import CommentForm
from blog.models import Article
from .models import Comment

from notifications.signals import notify
from django.contrib.auth.models import User


class CommentsView(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request, article_id, parent_comment_id=None):
        comment_form = CommentForm()
        parent_comment = Comment.objects.get(id=parent_comment_id)
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment': parent_comment,
        }
        return render(request, 'comment/reply.html', context)

    def post(self, request, article_id, parent_comment_id=None):
        article = get_object_or_404(Article, id=article_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                if not parent_comment.user.is_superuser and not parent_comment.user == request.user:
                    notify.send(
                        request.user,
                        recipient=new_comment.reply_to if new_comment.reply_to else parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
            else:
                new_comment.save()
                if not request.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='评论了你',
                        target=article,
                        action_object=new_comment,
                    )
            redirect_url = article.get_absolute_url() + '#comment_' + str(new_comment.id)
            return redirect(redirect_url)
        else:
            return HttpResponse("表单内容有误，请重新填写。")


comments_view = CommentsView.as_view()


def delete(request, article_id, comment_id):
    article = get_object_or_404(Article, id=article_id)
    comment = Comment.objects.get(id=comment_id)
    comment.content = ''
    comment.save(update_fields=['content'])
    return redirect(article)
