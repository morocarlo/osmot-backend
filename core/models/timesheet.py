# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description =  models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )

    def __str__(self):
        return "{}_{}".format(self.code, self.name)
          

class Timesheet(models.Model):
    day = models.DateField(blank=True, null=True)
    hour = models.FloatField(blank=True, null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self):
        return "{} at {} : {}".format(self.user, self.day, self.project)