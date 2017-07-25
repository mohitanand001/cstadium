from __future__ import unicode_literals

from django.db import models

from contest.models import Problem
from userprof.models import UserProfile
# Create your models here.


def upload_solution_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<username>/filename
    return 'solutions/user_{0}/{1}'.format(instance.user_associated, filename)


class SolutionCode(models.Model):
    problem_associated = models.ForeignKey(
        Problem, null='true', related_name='solutions_to_problem')
    user_associated = models.ForeignKey(
        UserProfile, null=True, related_name='user_so')
    code_text = models.FileField(null=True, upload_to=upload_solution_path)

    def __str__(self):
        return "solution_" + str(self.pk)
