from django.conf.urls import url
from django.contrib import admin
from chart.views import index, chart, post_times, deal_type

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', index),
    url(r'^chart/', chart),
    url(r'^post_times/', post_times),
    url(r'^deal_type/', deal_type),
]
