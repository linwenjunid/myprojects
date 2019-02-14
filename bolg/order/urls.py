from django.urls import path, include
from . import views


urlpatterns = (
    path('order_list/', views.order_list, name='order_list'),
    path('order/<int:order>/do_action/<int:action>', views.do_action, name='do_action'),
)