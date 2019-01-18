import xadmin
from xadmin.plugins.auth import UserAdmin
from .models import User


class UserInfoAdmin(UserAdmin):
    # 检索字段
    list_display = ('show_photo', 'username', 'phone_number', 'email', 'name', 'is_staff')
    list_display_links = ('show_photo', 'username',)
    # # 要显示的字段
    # list_display = ['id','username','phone_number' ,'email']
    # 分组过滤的字段
    # list_filter = ['is_staff',]
    # # ordering设置默认排序字段，负号表示降序排序
    # ordering = ('id',)
    # # list_per_page设置每页显示多少条记录，默认是100条
    # list_per_page = 50
    # # list_editable 设置默认可编辑字段
    # list_editable = ['phone_number',]

xadmin.site.unregister(User)
xadmin.site.register(User, UserInfoAdmin)