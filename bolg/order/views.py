from django.shortcuts import render
from .models import Order, OrderStep, OrderInstance
from django.shortcuts import get_object_or_404
from django.shortcuts import reverse, redirect
from django.db.models import Q


def order_list(request):
    ins = OrderInstance.objects.filter(code__in=[0, 1], action_user=request.user)
    pre_ins = OrderInstance.objects.filter(code=0, pre_action_user=request.user)
    return render(request, 'order/list.html', {'ins': ins,'pre_ins':pre_ins})


def do_action(request, order, action):
    if action==3:
        get_object_or_404(OrderInstance, pk=order, pre_action_user=request.user,code=0).go(action)
    else:
        get_object_or_404(OrderInstance, pk=order, action_user=request.user).go(action)

    return redirect("/admin/order/orderinstance/")
