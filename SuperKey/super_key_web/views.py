# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from super_key_api import views as api

# For delivering web UI to user
# Write data handling code in super_key_api.views

def login(request):
    template = 'login.html'
    return render(request, template, {})

def signup(request):
    template = 'signup.html'
    return render(request, template, {})