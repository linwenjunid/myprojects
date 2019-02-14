from django.db import models

STATUS = ((1,'开始'),(2,'结束'),(3,'串行'),(4,'并行'),(5,'或行'),(6,'合并'),(7,'合或'),(8,'分发'))
FLOW_STATUS = (('无效','无效'),('启用','启用'))


class Action(models.Model):
    action_name = models.CharField('处理方式', max_length=100)

    def __str__(self):
        return self.action_name

    class Meta:
        ordering = ['id']
        verbose_name = '处理方式'
        verbose_name_plural = '处理方式'


class Flow(models.Model):
    flow_name = models.CharField('流程', max_length=100)
    user = models.ForeignKey('user.User', verbose_name='创建者', on_delete=models.PROTECT, null=True, blank=True)
    flow_status = models.CharField('状态', choices=FLOW_STATUS, max_length=100, null=True)

    def __str__(self):
        return self.flow_name

    class Meta:
        ordering = ['id']
        verbose_name = '流程'
        verbose_name_plural = '流程'


class UserType(models.Model):
    type_name = models.CharField('用户组', max_length=100,help_text="用户组")
    user = models.ManyToManyField('user.User', verbose_name='组成员')

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ['id']
        verbose_name = '用户组'
        verbose_name_plural = '用户组'


class Status(models.Model):
    flow = models.ForeignKey(Flow, verbose_name='流程', on_delete=models.PROTECT)
    status_name = models.CharField('状态', max_length=100,help_text="流程所处的状态")
    status_type = models.IntegerField('状态类型', choices=STATUS, blank=True, null=True)
    user_type = models.ForeignKey(UserType, verbose_name='用户组',on_delete=models.PROTECT, blank=True, null=True,
                                  related_name = 'status_user_type')
    actions = models.ManyToManyField(Action, verbose_name="处理方式", blank=True,
                                     help_text="流程所处状态具有的处理方式:1:确认;2:回退;3:撤回;4:否决;")
    pre_user_type = models.ForeignKey(UserType, verbose_name='回退组', on_delete=models.PROTECT, blank=True, null=True,
                                  related_name='pre_status_user_type')


    def is_first(self):
        return self.status_type == 1

    def is_end(self):
        return self.status_type == 2

    def __str__(self):
        return self.flow.flow_name + '-' + self.status_name

    class Meta:
        ordering = ['id']
        verbose_name = '状态'
        verbose_name_plural = '状态'


class Step(models.Model):
    flow = models.ForeignKey(Flow, verbose_name='流程', on_delete=models.PROTECT)
    step_name = models.CharField('步骤', max_length=100)
    from_status = models.ForeignKey(Status, verbose_name='开始状态', on_delete=models.PROTECT, related_name='from_Step')
    to_status = models.ForeignKey(Status, verbose_name='结束状态', on_delete=models.PROTECT, related_name='to_Step')
    action = models.ForeignKey(Action, verbose_name='处理方式', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.step_name

    class Meta:
        ordering = ['flow__id','from_status','action']
        verbose_name = '步骤'
        verbose_name_plural = '步骤'