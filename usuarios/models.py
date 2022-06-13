from random import choice
from string import ascii_lowercase, ascii_uppercase, digits
from django.db import models
from django.db.models.fields.json import JSONField

# Create your models here.

def generate_token(user, size=70, chars=ascii_uppercase + ascii_lowercase + digits):
    return str(user.id) + "_" + ''.join(choice(chars) for x in range(size))

def get_user_json(user):
    return {
        'pk': user.pk,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'is_active': user.is_active,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }


class UserExtraData(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='static/user_images', null=True, blank=True)

    # lista en JSON de los ids de los articulos leidos
    read_articles = JSONField(default=list)

    
    def __str__(self):
        return self.user.username

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'phone': self.phone,
            'birth_date': self.birth_date,
            'image': self.image.url if self.image else None,
            'read_articles': self.read_articles,
        }


class UserToken(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'token': self.token,
            'created_at': self.created_at,
        }
