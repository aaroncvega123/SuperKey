# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from .models import User, AuthKey, ThirdPartyCredentials
import datetime

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
        password_hash = hash_string(password)

        user  = User.objects.all() \
            .filter(email = email_address) \
            .filter(password_hash = password_hash) \
            .first()

        if user:
            auth_key = create_auth_key(email_address, password_hash)
            response = {
                'status': 'OK',
                'auth_key': auth_key,
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
        password_hash = hash_string(password)

        if account_exists(email_address):
            response = {
                'status': 'ACCOUNT EXISTS'
            }
        else:
            user = User(
                email = email_address,
                password_hash = password_hash
            )
            user.save()
            auth_key = create_auth_key(email_address, password_hash)
            response = {
                'status': 'OK',
                'auth_key': auth_key,
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
        response = {'status': 'OK'}


    return JsonResponse(response)

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
    new_auth_key_string = ''

    if user:
        user_id = user.id
        auth_key = AuthKey.objects.all() \
            .filter(user_id = user_id) \
            .first()
        date = datetime.datetime.now()
        date_string = str(date)
        new_auth_key_string = hash_string(email_address + password_hash + date_string)

        if auth_key:
            auth_key.auth_key = new_auth_key_string
            auth_key.create_date = date
            auth_key.save()
        else:
            auth_key = AuthKey(
                auth_key = new_auth_key_string,
                create_date = date,
                user_id = user
            )
            auth_key.save()

    return new_auth_key_string



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