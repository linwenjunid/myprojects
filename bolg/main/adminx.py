from .models import Article
from xadmin import views
from xadmin.layout import Fieldset, Layout, Container, Col
import xadmin


# @xadmin.sites.register(Article)
class ArticleAdmin:
    list_display = ("title", "user", "publish_time", "last_update_time")
    list_display_links = ("title",)
    search_fields = ["title"]

    # 过滤数据
    def queryset(self):
        qs = super(ArticleAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(user=self.request.user)

    # 保存动作
    def save_models(self):
        obj = self.new_obj
        if obj.user is None:
            obj.user = self.request.user
        obj.save()

    # 显示控制
    def get_form_layout(self):
        if self.request.user.is_superuser:
            self.form_layout = Layout(Container(Col('full',
                                                    Fieldset(
                                                        "", "title", "content", "user", css_class="unsort no_title"),
                                                    horizontal=True, span=12)
                                                ))
        else:
            self.form_layout = Layout(Container(Col('full',
                                                    Fieldset(
                                                        "", "title", "content", css_class="unsort no_title"),
                                                    horizontal=True, span=12)
                                                ))
        return super(ArticleAdmin, self).get_form_layout()


xadmin.site.register(Article, ArticleAdmin)


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    site_title = '学习'
    site_footer = '关于我'
    global_search_models = [Article, ]
    # 小图标
    global_models_icon = {
        Article: "glyphicon glyphicon-asterisk",
    }
    # 菜单折叠
    menu_style = 'default'  # 'accordion','default'