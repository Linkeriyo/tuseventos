from django.contrib import admin

from eventos.models import Article, ArticleType

# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleType)