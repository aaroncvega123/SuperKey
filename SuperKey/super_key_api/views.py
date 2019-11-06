# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from models import User

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
def signup(request):
    template = 'signup.html'
    request_method = request.method
    response = {}

    if(request_method == 'POST'):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        email_address = body['email']
        password = body['password']
        auth_key = hash_string(email_address + password)

        if account_exists(email_address):
            response = {
                'status': 'ACCOUNT EXISTS'
            }
        else:
            user = User(
                email = email_address,
                password_hash = hash_string(password)
            )

            user.save()

            response = {
                'status': 'OK',
                'auth_key': 'temp',
                'email': email_address,
                'user_id': user.id
            }

    return JsonResponse(response)

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

def create_auth_key(email_address, password_hash):
    #Check for existing user, and create a new auth_key

    user = User.objects.all() \
        .filter(email = email_address) \
        .filter(password_hash = password_hash) \
        .first()

    if user:
        auth_key = AuthKey.objects.all() \
            .filter(user_id == email_address)


def hash_string(input_string):
    hash_object = hashlib.md5(input_string.encode())
    return hash_object.hexdigest()

def account_exists(email_address):
    user  = User.objects.all() \
        .filter(email = email_address) \
        .first()

    if user:
        return True
    return False