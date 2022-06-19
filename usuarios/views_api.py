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


def check_user2(token, userdjango_id):
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
                    'token': user_token.token,
                    'username': user.username,
                    'email': user.email
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

        if check_user2(token, userdjango_id):
            userdjango = get_user_by_token(token)

            user_token = get_object_or_None(UserToken, user=userdjango)
            if user_token is None:
                response_data = {'result': 'ok',
                                 'message': 'user already logged out'}
            else:

                user_token.delete()
                response_data = {'result': 'ok',
                                 'message': 'user logged out successfully'}
        else:
            response_data = {'result': 'error',
                             'message': 'user was not logged in'}

        return JsonResponse(response_data)

    except Exception as e:
        response_data = {'errorcode': 'U0002',
                         'result': 'error', 'message': str(e)}
        return JsonResponse(response_data)


@csrf_exempt
def change_credentials(request):
    try:
        datos = json.loads(request.POST['data'])
        token = datos.get('token')
        userdjango_id = datos.get('user_id')
        password = datos.get('password')
        username = datos.get('username')
        email = datos.get('email')

        if check_user2(token, userdjango_id):
            userdjango = get_user_by_token(token)
            if userdjango is not None:
                if password is not None:
                    userdjango.set_password(password)
                    password_changed = True
                else:
                    password_changed = False

                if email is not None:
                    userdjango.email = email
                    email_changed = True
                else:
                    email_changed = False

                userdjango.save()
                
                response_data = {
                    'result': 'ok',
                    'message': 'user credentials changed successfully',
                    'password_changed': password_changed,
                    'email_changed': email_changed
                }
            else:
                response_data = {'result': 'error',
                                 'message': 'user not found'}
        else:
            response_data = {'result': 'error',
                             'message': 'user not logged in'}

        return JsonResponse(response_data)

    except Exception as e:
        response_data = {'errorcode': 'U0003',
                         'result': 'error', 'message': str(e)}
        return JsonResponse(response_data)


@csrf_exempt
def change_profile_picture(request):
    try:
        datos = json.loads(request.POST['data'])
        token = datos.get('token')
        user_id = datos.get('user_id')

        if check_user2(token, user_id):
            image = request.FILES['image']
            user = get_object_or_None(User, id=user_id)
            user.userextradata.image = image
            user.userextradata.save()

            return JsonResponse({'result': 'ok', 'message': 'profile picture changed successfully'})

        return JsonResponse({'result': 'error', 'message': 'user not logged in'})

    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def remove_profile_picture(request):
    try:
        datos = json.loads(request.POST['data'])
        token = datos.get('token')
        user_id = datos.get('user_id')

        if check_user2(token, user_id):
            user = get_object_or_None(User, id=user_id)
            user.userextradata.image = None
            user.userextradata.save()

            return JsonResponse({'result': 'ok', 'message': 'profile picture removed successfully'})

        return JsonResponse({'result': 'error', 'message': 'user not logged in'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def get_self_profile_picture(request):
    try:
        datos = json.loads(request.POST['data'])
        token = datos.get('token')
        user_id = datos.get('user_id')

        if check_user2(token, user_id):
            user = get_object_or_None(User, id=user_id)
            if user.userextradata.image is not None:
                image = user.userextradata.image.url
            else:
                image = None

            return JsonResponse({'result': 'ok', 'image': image})
        
        return JsonResponse({'result': 'error', 'message': 'user not logged in'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})
