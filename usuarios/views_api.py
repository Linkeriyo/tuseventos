from django.shortcuts import render
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from annoying.functions import get_object_or_None

from usuarios.models import UserToken, generate_token

# Create your views here.
def get_user_by_token(token):
    user_token = get_object_or_None(UserToken, token=token)

    if user_token is not None:
        return user_token.user
    else:
        return None


def get_userdjango_by_id2(userdjango_id):
    userdjango = get_object_or_None(User, pk=userdjango_id)

    return userdjango


def check_user2(token,userdjango_id):
    userdjango = get_userdjango_by_id2(userdjango_id)
    user_token = get_user_by_token(token)

    if (user_token is not None) and (userdjango is not None):
        if user_token == userdjango:
            return True
        else:
            return False
    else:
        return False

@csrf_exempt
def login(request):
    try:
        data = json.loads(request.POST['data'])
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                user_token = get_object_or_None(UserToken, user=user)

                if user_token is None:
                    user_token = UserToken.objects.create(
                        user=user,
                        token=generate_token(user)
                    )
                
                else:
                    user_token.token = generate_token(user)
                    user_token.save()

                return JsonResponse({
                    'result': 'ok',
                    'token': user_token.token
                })
                
            return JsonResponse({
                'result': 'error',
                'message': 'user_not_active'
            })
        
        return JsonResponse({
            'result': 'error',
            'message': 'user_not_found'
        })
    
    except Exception as e:
        return JsonResponse({
            'result': 'error',
            'message': str(e)
        })


@csrf_exempt
def register(request):
    try:
        data = json.loads(request.POST['data'])
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        if user is not None:
            if user.is_active:
                return login(request)
            
            return JsonResponse({
                'result': 'error',
                'message': 'user_not_active'
            })
        
        return JsonResponse({
            'result': 'error',
            'message': 'user_not_found'
        })

    except Exception as e:
        return JsonResponse({
            'result': 'error',
            'message': str(e)
        })


@csrf_exempt
def logout(request):
    try:
        try:
            datos = json.loads(request.POST['data'])
            token = datos.get('token')
            userdjango_id = datos.get('user_id')

        except Exception as e:
            token = request.POST['token']
            userdjango_id = request.POST['user_id']

        if check_user2(token,userdjango_id):
            userdjango = get_user_by_token(token)

            user_token = get_object_or_None(UserToken, user=userdjango)
            if user_token is None:
                response_data = {'result': 'ok', 'message': 'user already logged out'}
            else:

                user_token.delete()
                response_data = {'result': 'ok', 'message': 'user logged out successfully'}
        else:
            response_data = {'result': 'error', 'message': 'user was not logged in'}

        return JsonResponse(response_data)

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return JsonResponse(response_data)