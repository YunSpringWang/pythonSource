# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import *

app_name = 'users'
urlpatterns = [
    url(r'^$', home, name='login'),
    url(r'^logout/$', do_logout, name='logout'),
    url('get_validCode_img/', get_validCode_img),

]

