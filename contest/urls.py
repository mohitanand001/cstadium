from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^(?P<contest_id>\d+)/$', views.contest_view, name='contest_view'),
    url(r'^prob_upload/$', views.prob_upload, name='prob_upload'),
    url(r'^problem/(?P<problem_id>\d+)/$', views.problem_view, name='problem'),

]
