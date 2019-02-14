import xadmin
from .models import Order, OrderStep, OrderInstance, ZhouBao
from flow.models import Step, Status, Action
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import Q


class OrderInstanceInline(object):
    model = OrderInstance
    extra = 1
    style = "accordion"


class OrderAdmin:
    list_display = ("order_title", "user", "status", "create_time", "end_time")
    exclude = ('user', 'create_time', "end_time", "status")
    inlines = [OrderInstanceInline]

    def save_models(self):
        obj = self.new_obj
        if obj.user is None:
            obj.user = self.request.user
        if obj.status is None:
            obj.status = '开始'
            obj.save()
            obj.start_order()

        else:
            obj.save()


class OrderStepAdmin:
    list_display = ("id", "order","start_status","end_status", "action","action_uesr", "action_time")
    search_fields = ['order__order_title', ]
    list_filter = ["order__order_title"]

    def save_models(self):
        obj = self.new_obj
        if obj.action_uesr is None:
            obj.action_uesr = self.request.user
        obj.save()


class OrderInstanceAdmin:
    def myaction(self,instance):
        html = ""
        if instance.code == 0 and self.request.user==instance.action_user:
            url = "/order/" + str(instance.id) + "/do_action/6"
            html = html + "<a href='" + url + "'>接受</a>" + "&nbsp;"
        elif instance.code in [0,1] :
            for action in instance.status.actions.all():
                if instance.code == 0 and action.id==3 and self.request.user==instance.pre_action_user:
                    url = "/order/"+str(instance.id)+"/do_action/"+str(action.id)
                    html = html+"<a href='"+url+"'>"+action.action_name+"</a>"+"&nbsp;"
                elif action.id!=3 and self.request.user==instance.action_user:
                    url = "/order/" + str(instance.id) + "/do_action/" + str(action.id)
                    html = html + "<a href='" + url + "'>" + action.action_name + "</a>"+"&nbsp;"
        return html
    myaction.short_description = '操作'
    myaction.allow_tags = True
    myaction.is_column = True

    list_display = ("id", "order","flow","status","code","action_user","pre_action_user","myaction")
    search_fields = ['flow__flow_name',]

    def queryset(self):
        qs = super(OrderInstanceAdmin, self).queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(Q(Q(action_user=self.request.user)&Q(code__in=[0,1]))|
                              Q(Q(pre_action_user=self.request.user)&Q(code=0)))


class ZhouBaoAdmin:
    list_display = ("id", "order","start_status","end_status", "action","action_uesr", "action_time")
    search_fields = ['order__order_title', ]
    list_filter = ["order__order_title"]

    def save_models(self):
        obj = self.new_obj
        if obj.action_uesr is None:
            obj.action_uesr = self.request.user
        obj.save()

xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(OrderStep, OrderStepAdmin)
xadmin.site.register(OrderInstance, OrderInstanceAdmin)
xadmin.site.register(ZhouBao, ZhouBaoAdmin)