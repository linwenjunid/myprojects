from __future__ import absolute_import, unicode_literals
from django.utils.translation import ugettext_lazy as _
import xadmin
from django_celery_results.models import TaskResult
from django_celery_beat.models import IntervalSchedule,CrontabSchedule,PeriodicTask
from celery import current_app
from django.forms.widgets import Select
from celery.utils import cached_property
from django import forms
from kombu.utils.json import loads


class TaskSelectWidget(Select):
    """Widget that lets you choose between task names."""

    celery_app = current_app
    _choices = None

    def tasks_as_choices(self):
        _ = self._modules  # noqa
        tasks = list(sorted(name for name in self.celery_app.tasks
                            if not name.startswith('celery.')))
        return (('', ''), ) + tuple(zip(tasks, tasks))

    @property
    def choices(self):
        if self._choices is None:
            self._choices = self.tasks_as_choices()
        return self._choices

    @choices.setter
    def choices(self, _):
        # ChoiceField.__init__ sets ``self.choices = choices``
        # which would override ours.
        pass

    @cached_property
    def _modules(self):
        self.celery_app.loader.import_default_modules()


class TaskChoiceField(forms.ChoiceField):
    """Field that lets you choose between task names."""

    widget = TaskSelectWidget

    def valid_value(self, value):
        return True


class MyForm(forms.ModelForm):
    # 任务名下拉框替换原模型的字符框
    task = TaskChoiceField(
        label=_('Task'),
        required=False,
    )

    class Meta:
        model = PeriodicTask
        exclude = ()


class PeriodicTaskAdmin:
    form = MyForm
    model = PeriodicTask


class TaskResultAdmin:
    list_display = ("task_id", "task_name","status","result")


xadmin.site.register(TaskResult,TaskResultAdmin)
xadmin.site.register(IntervalSchedule)
xadmin.site.register(CrontabSchedule)
xadmin.site.register(PeriodicTask,PeriodicTaskAdmin)
