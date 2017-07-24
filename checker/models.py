from __future__ import unicode_literals

from django.db import models

from contest.models import Problem
from userprof.models import UserProfile
# Create your models here.


class SolutionCode(models.Model):
    problem_associated = models.ForeignKey(Problem,null='true',related_name='solutions_to_problem')
    user_associated    = models.ForeignKey(UserProfile,null=True,related_name='user_so')
    code_text  = models.FileField(null=True)

    def __str__(self):
        return "solution_"+str(self.pk)
