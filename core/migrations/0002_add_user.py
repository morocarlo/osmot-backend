# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.hashers import make_password

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('core', '0001_initial'),
    ]

    def create_admin_user(apps, schema_editor):
        User = apps.get_registered_model('auth', 'User')
        if not User.objects.filter(username='admin').exists():
            admin = User(
                username='admin',
                email='a@a.it',
                password=make_password('admin'),
                is_superuser=True,
                is_staff=True
            )
            admin.save()

    operations = [
        migrations.RunPython(create_admin_user),
    ]
