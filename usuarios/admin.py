from django.contrib import admin

from usuarios.models import UserExtraData, UserToken

# Register your models here.
admin.site.register(UserExtraData)
admin.site.register(UserToken)