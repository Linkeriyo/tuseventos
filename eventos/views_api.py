import json

from django.http import JsonResponse
from eventos.models import Article, FavoriteArticle, RemindMeArticle
from django.core.paginator import Paginator
from usuarios.views_api import check_user2
from django.views.decorators.csrf import csrf_exempt
from annoying.functions import get_object_or_None
from django.contrib.auth.models import User

# Create your views here.
@csrf_exempt
def get_articles(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']
        page = data['page']

        if check_user2(token, user_id):
            articles = Article.objects.all().order_by('-date').annotate

            paginator = Paginator(articles, 10)
            articles = paginator.page(page)

            articles_dict = []

            for article in articles:
                article_dict = article.to_dict()
                if FavoriteArticle.objects.filter(user=user_id, article=article.id).exists():
                    article_dict['is_favorite'] = True
                else:
                    article_dict['is_favorite'] = False
                articles_dict.append(article_dict)

            return JsonResponse({'result': 'ok', 'articles': articles_dict})
        
        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def get_favorite_articles(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']
        page = data['page']
        
        if check_user2(token, user_id):
            fav_articles = FavoriteArticle.objects.filter(user__id=user_id).order_by('-article__date')

            paginator = Paginator(fav_articles, 10)
            fav_articles = paginator.page(page)
            
            articles_dict = []
            
            for fav_article in fav_articles:
                articles_dict.append(fav_article.article.to_dict())
            
            return JsonResponse({'result': 'ok', 'articles': articles_dict})
        
        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def get_remind_me_articles(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']
        page = data['page']
        
        if check_user2(token, user_id):
            remind_me_articles = RemindMeArticle.objects.filter(user__id=user_id).order_by('-article__date')
            
            paginator = Paginator(remind_me_articles, 10)
            remind_me_articles = paginator.page(page)
            
            articles_dict = []
            
            for remind_me_article in remind_me_articles:
                articles_dict.append(remind_me_article.article.to_dict())
            
            return JsonResponse({'result': 'ok', 'articles': articles_dict})
        
        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def get_article(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']
        article_id = data['article_id']
        
        if check_user2(token, user_id):
            article = get_object_or_None(Article, id=article_id)

            if article:
                return JsonResponse({'result': 'ok', 'article': article.to_dict()})

            return JsonResponse({'result': 'error', 'message': 'Artículo no encontrado'})
        
        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def add_favorite_article(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']
        article_id = data['article_id']
        
        if check_user2(token, user_id):
            article = get_object_or_None(Article, id=article_id)
            user = get_object_or_None(User, id=user_id)
            
            if article and user:
                fav_article = get_object_or_None(FavoriteArticle, article__id=article_id, user__id=user_id)
                
                if fav_article:
                    return JsonResponse({'result': 'error', 'message': 'Artículo ya agregado a favoritos'})
                
                fav_article = FavoriteArticle(article=article, user=user)
                fav_article.save()
                
                return JsonResponse({'result': 'ok', 'message': 'Artículo agregado a favoritos'})
            
            return JsonResponse({'result': 'error', 'message': 'Artículo o usuario no encontrado'})
        
        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def remove_favorite_article(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']
        article_id = data['article_id']
        
        if check_user2(token, user_id):
            article = get_object_or_None(Article, id=article_id)
            user = get_object_or_None(User, id=user_id)
            
            if article and user:
                fav_article = get_object_or_None(FavoriteArticle, article__id=article_id, user__id=user_id)
                
                if fav_article:
                    fav_article.delete()
                    
                    return JsonResponse({'result': 'ok', 'message': 'Artículo eliminado de favoritos'})
                
                return JsonResponse({'result': 'error', 'message': 'Artículo no encontrado'})
            
            return JsonResponse({'result': 'error', 'message': 'Artículo o usuario no encontrado'})
        
        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})
