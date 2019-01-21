import xadmin
from xadmin.plugins.auth import UserAdmin
from .models import User


class UserInfoAdmin(UserAdmin):
    # 检索字段
    list_display = ('show_photo', 'username', 'phone_number', 'email', 'name', 'is_staff')
    list_display_links = ('show_photo', 'username',)


xadmin.site.unregister(User)
xadmin.site.register(User, UserInfoAdmin)