from django.conf.urls import url
from . import views
from django.urls import path
app_name="chromebook"
urlpatterns = [
    url('host_list/', views.HostListView, name='host_list'),
    path('CheckServerDetailsView/', views.CheckServerDetailsView, name='CheckServerDetailsView'),
]