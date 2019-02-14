import xadmin
from .models import Action, Flow, Status, Step, UserType


class ActionAdmin:
    list_display = ("id", "action_name")
    list_editable = ('action_name',)


class StatusInline(object):
    model = Status
    extra = 1
    style = "accordion"


class FlowAdmin:
    list_display = ("id", "flow_name", 'flow_status', 'user')
    list_editable = ('flow_name', 'flow_status')
    inlines = [StatusInline]

    def save_models(self):
        obj = self.new_obj
        if obj.user is None:
            obj.user = self.request.user
        obj.save()


class StatusAdmin:
    list_display = ("id", "status_name", 'status_type', 'user_type', 'pre_user_type', 'flow', 'actions')
    list_editable = ('status_name', 'status_type', 'user_type', 'pre_user_type',)
    search_fields = ["status_name",'flow__flow_name']


class StepAdmin:
    list_display = ("step_name",'from_status', 'to_status', 'flow', 'action')
    list_editable = ('step_name','action')
    list_filter = ["action"]


class UserTypeAdmin:
    list_display = ('type_name','user')

xadmin.site.register(Action, ActionAdmin)
xadmin.site.register(Flow, FlowAdmin)
xadmin.site.register(Status, StatusAdmin)
xadmin.site.register(Step, StepAdmin)
xadmin.site.register(UserType, UserTypeAdmin)