from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.article_list, name='index'),
    path('search', views.article_list, name='search'),
    path('tag/<str:name>', views.article_list, name='tag'),
    path('category/<str:name>', views.article_list, name='category'),
    path('article/<int:id>', views.article_detail, name='article'),
    path('api', views.page_ajax, name='api'),
    path('api/search/', views.MySearchView(), name='api_search'),
]
