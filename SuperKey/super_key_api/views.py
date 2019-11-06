# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# API for data used in front ends

@csrf_exempt
def login(request):
    request_method = request.method
    response = {}

    if(request_method == 'POST'):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        email_address = body['email']
        password = body['password']

        user  = User.objects.all() \
            .filter(email = email_address) \
            .filter(password_hash = hash_string(password)) \
            .first()

        if user:
            response = {
                'status': 'OK',
                'auth_key': user.auth_key,
                'email': user.email,
                'user_id': user.id
            }
        else:
            response = {
                'status': 'NOT FOUND'
            }

    return JsonResponse(response)

@csrf_exempt
def new_user(request):
    return JsonResponse({'status': 'OK'})

def logout(request):
    return JsonResponse({'status': 'OK'})

def authenticate(request):
    request_method = request.method
    response = {}

    if(request_method == 'POST'):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)


        return JsonResponse({'status': 'OK'})

def third_party_credentials(request):
    return JsonResponse({'status': 'OK'})


#Helper methods

def auth_key_is_valid(auth_key):
    auth_key  = AuthKey.objects.all() \
        .filter(auth_key = auth_key) \
        .first()

    if auth_key:
        return True
    return False