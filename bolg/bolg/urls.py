"""bolg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from __future__ import absolute_import, unicode_literals
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls'), name='ckeditor'),
    path('captcha/', include('captcha.urls'), name='captcha'),
    path('',include('order.urls'), name='order'),
    path('wc/',include('echart.urls'), name='wc')
    ] + static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    ) + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

