import xadmin
from xadmin import views
from .views import scatter3DView, line3dView,gridView
# Register your models here.
xadmin.site.register_view(r'scatter/$', scatter3DView, name='scatter')
xadmin.site.register_view(r'line/$', line3dView, name='line')
xadmin.site.register_view(r'grid/$', gridView, name='grid')