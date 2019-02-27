from .models import Comments
import xadmin
from .views import CommentsView

xadmin.site.register_view(r'treedemo/$', CommentsView, name='treedemo')


@xadmin.sites.register(Comments)
class CommentsAdmin:
    list_display = ( "post", "user", "content", "parent","created_time")
    list_display_links = ("content",)
    search_fields = ["content"]


