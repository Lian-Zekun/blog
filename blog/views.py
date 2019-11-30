import json
from urllib import parse

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from haystack.views import SearchView

from comment.forms import CommentForm
from comment.models import Comment
from .models import *


def article_list(request, name=None):
    if request.path == '/search':
        name = 'search'
    return render(request, 'blog/article_list.html', context={'title': name})


def about(request):
    return render(request, 'about.html')


def robots(request):
    return render(request, 'robots.txt')


def page_not_find(request, exception):
    """全局404页面处理"""
    return render(request, 'error.html', status=404)


def page_error(request):
    """全局500页面处理"""
    return render(request, 'error.html', status=500)


def resources_not_available(request, exception):
    """全局500页面处理"""
    return render(request, 'error.html', status=403)


@csrf_exempt
def page_ajax(request):
    if request.method == 'GET':
        page_num = request.GET.get('page_num')
        path = parse.unquote(request.GET.get('path')).split('/')
        title = path[-2]
        name = path[-1]
        if title == 'tag':
            queryset = Article.objects.filter(tags__name=name)
        elif title == 'category':
            queryset = Article.objects.filter(category__name=name)
        else:
            queryset = Article.objects.all()
        paginator = Paginator(queryset, 5)
        page_list = paginator.page(int(page_num)).object_list

        result = []
        for page in page_list:
            page_result = []
            time = page.publish_time.strftime('%Y-%m-%d')
            page_result.append(time)
            time = page.publish_time.strftime('%H:%M:%S')
            page_result.append(time)
            page_result.append(page.title)
            page_result.append(str(page.pic))
            page_result.append(page.excerpt)
            page_result.append(page.read_num)
            page_result.append(page.id)
            # page_result.append(page.comments.count)
            result.append(page_result)
        context = {
            'result': result,
            'page_num': page_num,
            'num_pages': paginator.num_pages
        }
        return HttpResponse(json.dumps(context))


class MySearchView(SearchView):
    def create_response(self):
        context = super().get_context()
        result = []
        for page in context['page'].object_list:
            page_result = []
            time = page.object.publish_time.strftime('%Y-%m-%d')
            page_result.append(time)
            time = page.object.publish_time.strftime('%H:%M:%S')
            page_result.append(time)
            page_result.append(page.object.title)
            page_result.append(str(page.object.pic))
            page_result.append(page.object.excerpt)
            page_result.append(page.object.read_num)
            page_result.append(page.object.id)
            # page_result.append(page.comments.count)
            result.append(page_result)
        context['result'] = result
        context['page_num'] = int(self.request.GET.get('page', 1))
        context['num_pages'] = context['paginator'].num_pages
        del context['form']
        del context['page']
        del context['paginator']
        return HttpResponse(json.dumps(context))


class ArticleDetailView(DetailView):
    queryset = Article.objects.all()
    context_object_name = 'article'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.read_num += 1
        obj.save(update_fields=['read_num'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # comments = get_object_or_404(Comment, article=self.kwargs.get(self.pk_url_kwarg))
        comments = Comment.objects.filter(article=self.kwargs.get(self.pk_url_kwarg))
        time = self.object.publish_time
        pre_article = Article.objects.filter(publish_time__lt=time).order_by('-publish_time')
        # 过滤出id大的文章
        next_article = Article.objects.filter(publish_time__gt=time).order_by('publish_time')
        # 取出相邻前一篇文章
        pre_article = pre_article[0] if pre_article.count() > 0 else None
        # 取出相邻后一篇文章
        next_article = next_article[0] if next_article.count() > 0 else None

        context['tags'] = self.object.tags.all()
        context['comment_form'] = CommentForm()
        context['comments'] = comments
        context['pre_article'] = pre_article
        context['next_article'] = next_article
        return context


article_detail = ArticleDetailView.as_view()
