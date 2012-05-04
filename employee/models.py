from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Employee(models.Model):
    user        = models.OneToOneField(User)
    employee_id = models.IntegerField()

    def __unicode__(self):
        return self.user.first_name