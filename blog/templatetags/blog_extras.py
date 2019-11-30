from django import template

from ..models import *

register = template.Library()


@register.inclusion_tag('header.html', takes_context=True)
def blog_header(context):
    return {
        'categories': Category.objects.all(),
        'user': context['user'],
        'request': context['request']
    }


@register.inclusion_tag('blog/inclusions/tags.html', takes_context=True)
def get_tags(context):
    return {'tags': Tag.objects.all()}


@register.inclusion_tag('blog/inclusions/categories.html', takes_context=True)
def get_categories(context):
    return {'categories': Category.objects.all()}


@register.inclusion_tag('blog/inclusions/timeline.html', takes_context=True)
def new_article(context):
    return {'articles': Article.objects.all()[:5]}


@register.inclusion_tag('blog/inclusions/timeline.html', takes_context=True)
def get_articles(context):
    return {'articles': context['articles']}
