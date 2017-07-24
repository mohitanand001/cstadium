from __future__ import unicode_literals
from django.db import models

from userprof.models import UserProfile
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE
from ckeditor.fields import RichTextField

import os

# Create your models here.

class Contest(models.Model):
    contest_id = models.IntegerField(unique=True)
    name_of_contest = models.CharField(max_length=20)
    rated_or_test = models.BooleanField(default=False)
    number_of_problems = models.IntegerField(default=0)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    duration_of_content = models.FloatField(default=0)
    live = models.BooleanField(default=False)

    def __str__(self):
        return self.name_of_contest

def test_file_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<problem_id>/<filename>
    return 'problems/problem_{0}/{1}'.format(instance.problem_id, filename)

def sample_io_upload(instance,filename):
    return 'problem_{0}/{1}'.format(instance.problem_id, filename)

class Problem(models.Model):
    problem_id = models.IntegerField(primary_key=True)
    name_of_problem = models.CharField(unique=True,max_length=40)
    test_files = models.FileField(upload_to=test_file_upload,null=True)
    statement = RichTextField()
    contest = models.ForeignKey(Contest,null=True,related_name='problems')
    time_limit = models.IntegerField(default=1)
    max_score = models.IntegerField(default=100)
    number_of_correct_submissions = models.IntegerField(default=0)
    solved_by_whom = models.ManyToManyField(UserProfile,)

    def __str__(self):
        return self.name_of_problem
    

