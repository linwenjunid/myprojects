import xadmin
from .views import scatter3DView, line3dView, gridView, wordcloudView, neo4jView
from xadmin.views.website import IndexView
from .models import xchart
# Register your models here.
xadmin.site.register_view(r'scatter/$', scatter3DView, name='scatter')
xadmin.site.register_view(r'line/$', line3dView, name='line')
xadmin.site.register_view(r'grid/$', gridView, name='grid')
xadmin.site.register_view(r'wordcloud/$', wordcloudView, name='wordcloud')
xadmin.site.register_view(r'neo4j/$', neo4jView, name='neo4j')


@xadmin.sites.register(IndexView)
class MainDashboard(object):

    def get_widgets(self):
        # widgets = super(IndexView, self).get_widgets()
        # 拆成两列
        # widgets = [[widgets[0][1],],[widgets[0][2],]]
        return super(IndexView, self).get_widgets()


class xchartAdmin:
    list_display = ("data","xcount")
    aggregate_fields = {"xcount": "sum"}
    data_charts = {
        "xcount": {'title': u"xcount", "x-field": "data", "y-field": ("xcount",), "order": ('data',)},
    }


xadmin.site.register(xchart,xchartAdmin)