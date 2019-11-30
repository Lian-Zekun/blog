from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Article


class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'unread_notices'
    # 模板位置
    template_name = 'notice/list.html'
    # 登录重定向
    login_url = '/accounts/login'

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data(**kwargs)
        read_notices = self.request.user.notifications.read()
        content['read_notices'] = read_notices if read_notices else None
        return content


comment_notice_list = CommentNoticeListView.as_view()


class CommentNoticeUpdateView(View):
    """更新通知状态"""
    # 处理 get 请求
    def get(self, request, *args, **kwargs):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            article = get_object_or_404(Article, id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')


comment_notice_update = CommentNoticeUpdateView.as_view()
