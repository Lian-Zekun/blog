"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications.urls
import xadmin

from django.urls import path, re_path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
# from django.views import static
# from django.conf import settings

from blog.models import Article, Category, Tag
from blog.views import about, robots

handler404 = 'blog.views.page_not_find'
handler500 = 'blog.views.page_error'
handler403 = 'blog.views.resources_not_available'

article_dict = {
    'queryset': Article.objects.all(),
    'date_field': 'modified_time',
}
category_dict = {'queryset': Category.objects.all()}
tag_dict = {'queryset': Tag.objects.all()}

sitemaps = {
    'article': GenericSitemap(article_dict, priority=0.7, changefreq='monthly'),
    'category': GenericSitemap(category_dict, priority=0.3, changefreq='monthly'),
    'tag': GenericSitemap(tag_dict, priority=0.3, changefreq='monthly'),
}

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('mdeditor/', include('mdeditor.urls')),
    path('accounts/', include('allauth.urls')),
    path('notifications/', include(notifications.urls, namespace='notifications')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include('blog.urls', namespace='blog')),
    path('notice/', include('notice.urls', namespace='notice')),
    path('api/comment/', include('comment.urls', namespace='comment')),
    path('about', about, name='about'),
    path('robots.txt', robots)
    # re_path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT }, name='static'),
]

from django.conf import settings
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
