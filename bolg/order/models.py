from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from flow.models import Step, Status, Action, Flow, UserType
from django.shortcuts import get_object_or_404
from django.utils import timezone as datetime
from django.db import connection


ORDER_STATUS = (('开始', '开始'), ('进行中', '进行中'), ('结束', '结束'))


class Order(models.Model):
    order_title = models.CharField('标题', max_length=100)
    order_content = RichTextUploadingField(
        verbose_name='内容', config_name='Code')
    user = models.ForeignKey(
        'user.User',
        verbose_name='发起人',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='order_create_uesr')
    flow = models.ForeignKey(
        'flow.Flow',
        verbose_name='流程',
        on_delete=models.PROTECT)
    status = models.CharField(
        '工单状态',
        choices=ORDER_STATUS,
        max_length=100,
        null=True,
        blank=True)
    create_time = models.DateTimeField(
        '工单创建时间', auto_now_add=True, null=True, blank=True)
    end_time = models.DateTimeField('工单结束时间', null=True, blank=True)

    def start_order(self):
        status = None
        for s in Status.objects.filter(flow=self.flow).all():
            i = OrderInstance()
            i.order = self
            i.flow = self.flow
            i.status = s
            if not s.user_type is None:
                i.action_user = s.user_type.user.all()[0]
            if not s.pre_user_type is None:
                i.pre_action_user = s.pre_user_type.user.all()[0]
            if s.status_type == 1:
                i.code = 0
                i.save()
                status = i
            else:
                i.save()
        status.go(1)

    def __str__(self):
        return self.order_title

    class Meta:
        ordering = ['flow__id']
        verbose_name = '工单'
        verbose_name_plural = '工单'


class OrderInstance(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='工单',
        on_delete=models.PROTECT)
    flow = models.ForeignKey(Flow, verbose_name='流程', on_delete=models.PROTECT)
    status = models.ForeignKey(
        Status,
        verbose_name='节点',
        on_delete=models.PROTECT)
    code = models.IntegerField('状态', null=True, blank=True)
    action_user = models.ForeignKey("user.User", verbose_name='当前操作用户', on_delete=models.PROTECT, blank=True, null=True,
                                    related_name='action_user')
    pre_action_user = models.ForeignKey("user.User", verbose_name='当前回退用户', on_delete=models.PROTECT, blank=True, null=True,
                                        related_name='pre_action_user')

    def saveOrderStep(self, action):
        os = OrderStep()
        if action in [2, 3]:
            step = get_object_or_404(
                Step, action=1, flow=self.flow, to_status=self.status)
            os.start_status = step.to_status
            os.end_status = step.from_status
        elif action in [6, 5]:
            os.start_status = self.status
            os.end_status = self.status
        else:
            step = get_object_or_404(
                Step,
                action=action,
                flow=self.flow,
                from_status=self.status)
            os.start_status = step.from_status
            os.end_status = step.to_status
        os.order = self.order
        os.flow = self.flow
        os.action = Action.objects.get(pk=action)
        os.action_uesr = self.pre_action_user if action == 3 else self.action_user
        os.action_time = datetime.now()
        os.save()

    def go(self, action):
        if action == 1:
            # 完成
            self.complete()
        elif action == 2:
            # 回退
            self.back()
        elif action == 3:
            # 撤回
            self.back()
        elif action == 5:
            # 保存
            self.hold()
        elif action == 6:
            # 接受
            self.accept()
        else:
            # 其他
            self.other(action)
        self.saveOrderStep(action)

    def accept(self):
        # 接受
        self.code = 1
        self.save()

    def complete(self):
        # 完成
        self.code = 2
        self.save()
        step = get_object_or_404(
            Step,
            action=1,
            flow=self.flow,
            from_status=self.status)
        i2 = get_object_or_404(
            OrderInstance,
            order=self.order,
            status=step.to_status)
        if step.to_status.status_type == 2:
            # 结束
            i2.code = 2
            i2.save()
            self.order.status = '结束'
            self.order.end_time = datetime.now()
            self.order.save()
        elif step.to_status.status_type == 4:
            # 并行
            i2.code = 2
            i2.save()
            for s in Step.objects.filter(
                    action=1, flow=self.flow, from_status=step.to_status).all():
                si = get_object_or_404(
                    OrderInstance, order=self.order, status=s.to_status)
                si.code = 0
                si.save()
        elif step.to_status.status_type == 6:
            # 合并
            sql = """
                SELECT count(*) nums FROM order_orderinstance b
                WHERE b.status_id IN (
                SELECT a.from_status_id FROM flow_step a WHERE a.action_id = 1 AND a.flow_id = {} AND a.to_status_id = {})
                AND b.order_id = {}
                AND b.`code` <> 2
            """.format(self.flow.id, step.to_status.id, self.order.id)
            with connection.cursor() as c:
                c.execute(sql)
                d = c.fetchone()
                if d[0]==0:
                    i2.code = 2
                    i2.save()
                    s2 = get_object_or_404(
                        Step,
                        action=1,
                        flow=self.flow,
                        from_status=step.to_status)
                    si = get_object_or_404(
                        OrderInstance,
                        order=self.order,
                        status=s2.to_status)
                    si.code = 0
                    si.save()
        else:
            i2.code = 0
            i2.save()

    def back(self):
        self.code = None
        self.save()
        step = get_object_or_404(
            Step,
            action=1,
            flow=self.flow,
            to_status=self.status)
        i2 = get_object_or_404(
            OrderInstance,
            order=self.order,
            status=step.from_status)
        i2.code = 1
        i2.save()

    def hold(self):
        pass

    def other(self, action):
        # 其他
        self.code = 2
        self.save()
        step = get_object_or_404(
            Step,
            action=action,
            flow=self.flow,
            from_status=self.status)
        i2 = get_object_or_404(
            OrderInstance,
            order=self.order,
            status=step.to_status)
        i2.code = 0
        i2.save()

    def __str__(self):
        return self.status.status_name

    class Meta:
        ordering = ['order__id', 'status__id']
        verbose_name = '待办'
        verbose_name_plural = '待办'


class OrderStep(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='工单',
        on_delete=models.PROTECT)
    flow = models.ForeignKey(
        'flow.Flow',
        verbose_name='流程',
        on_delete=models.PROTECT)
    start_status = models.ForeignKey(
        'flow.Status',
        verbose_name='开始状态',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='start_status')
    end_status = models.ForeignKey(
        'flow.Status',
        verbose_name='结束状态',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='end_status')
    action = models.ForeignKey(
        'flow.Action',
        verbose_name="处理方式",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text="流程所处状态具有的处理方式:1:完成;2:回退;3:确认;4:否决;")
    action_uesr = models.ForeignKey(
        'user.User',
        verbose_name='操作人',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='action_uesr')
    action_time = models.DateTimeField('时间', blank=True, null=True)

    def __str__(self):
        return self.flow.flow_name

    class Meta:
        ordering = ['id']
        verbose_name = '详情'
        verbose_name_plural = '详情'


class ZhouBaoManager(models.Manager):
    def get_queryset(self):
        return super(ZhouBaoManager,self).get_queryset().filter(flow=3)


class ZhouBao(OrderStep):

    objects = ZhouBaoManager()

    class Meta:
        proxy = True
        verbose_name = '周报'
        verbose_name_plural = '周报'