from django.conf.urls import url,include
from . import views


urlpatterns = [
	url(r'^problem/submit/(?P<problem_id>\d+)',views.solution_submit,name='solution_submit'),

]
    