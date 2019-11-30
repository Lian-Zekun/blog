import xadmin
from xadmin import views
from .models import *


class ArticleAdmin(object):
    model_icon = 'fa fa-edit'  # 菜单图标
    # form = ArticleForm
    list_display = ('title', 'category', 'publish_time', 'modified_time')  # 显示内容
    list_filter = ('category', 'tags')  # 分类筛选
    list_per_page = 20  # 分页大小
    search_fields = ('title', 'tags', 'content')  # 搜索内容


class TagAdmin(object):
    model_icon = 'fa fa-tags'
    list_display = ('name', 'article_count')


class CategoryAdmin(object):
    model_icon = 'fa fa-th - large'
    list_display = ('name', 'article_count')

    def article_count(self, obj):
        return Article.objects.filter(category=obj).count()


# xadmin设置
class GlobalSetting(object):
    site_title = '博客管理'  # 顶部标题
    site_footer = '博客管理'  # 底部标题
    menu_style = 'accordion'  # 菜单可折叠


class BaseSetting(object):
    enable_themes = True  # 启用主题管理器
    use_bootswatch = True  # 使用主题


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Category, CategoryAdmin)

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
