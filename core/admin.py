# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models.timesheet import Timesheet, Project
# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'start_date', 'end_date' )
    search_fields = (
        'name',
        'code'
    )

@admin.register(Timesheet)
class TimesheettAdmin(admin.ModelAdmin):
    list_filter = ('user', 'project', 'day',)
    list_display = ('user', 'project', 'day', 'hour' )
    search_fields = (
        'project__name',
        'project__code'
    )