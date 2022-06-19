from django.contrib import admin

from eventos.models import Article, ArticleComment, ArticleImage, ArticleType

# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleType)
admin.site.register(ArticleImage)
admin.site.register(ArticleComment)