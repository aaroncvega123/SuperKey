# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)

class AuthKey(models.Model):
    auth_key = models.CharField(max_length=255, default=None)
    create_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class ThirdPartyCredentials(models.Model):
    identity_string = models.CharField(max_length=255)
    encrypted_passsword = models.CharField(max_length=255)
    note = models.CharField(max_length=500, default='')