from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User

# from contest.models import Problem
# Create your models here.



def user_images_path(instance, filename):
    from django.template.defaultfilters import slugify
    filename, ext = os.path.splitext(filename)
    return 'avatars/user_{0}/{1}{2}'.format(instance.user.id, slugify(filename), ext)


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name="userprofile")
    user_avatar = models.ImageField(upload_to=user_images_path, blank=True, null=True)
    age = models.IntegerField(default = 10)

    def avatar(self, size=36):
        if self.user_avatar:
            return self.user_avatar.url

        for account in self.user.socialaccount_set.all():
            if 'avatar_url' in account.extra_data:
                return account.extra_data['avatar_url']
            elif 'picture' in account.extra_data:
                return account.extra_data['picture']

    def __unicode__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = UserProfile(user=user)
        profile.save()

post_save.connect(create_profile, sender=User)

