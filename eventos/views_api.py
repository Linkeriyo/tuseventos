import json

from django.http import JsonResponse
from eventos.models import Article, ArticleComment, ArticleType, FavoriteArticle
from django.core.paginator import Paginator
from usuarios.models import UserExtraData
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
        try:
            type_id = data['type_id']
        except:
            type_id = None

        if check_user2(token, user_id):
            if type_id is not None:
                articles = Article.objects.filter(article_type__id=type_id).order_by('-date_created')
            else:
                articles = Article.objects.all().order_by('-date_created')

            paginator = Paginator(articles, 10)
            articles = paginator.page(page)

            articles_dict = []

            for article in articles:
                article_dict = article.to_dict()
                if FavoriteArticle.objects.filter(user=user_id, article=article.id).count() > 0:
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
        try:
            type_id = data['type_id']
        except:
            type_id = None
        
        if check_user2(token, user_id):
            if type_id is not None:
                fav_articles = FavoriteArticle.objects.filter(user=user_id, article__article_type__id=type_id).order_by('-article__date_created')
            else:
                fav_articles = FavoriteArticle.objects.filter(user=user_id).order_by('-article__date_created')

            paginator = Paginator(fav_articles, 10)
            fav_articles = paginator.page(page)
            
            articles_dict = []
            
            for fav_article in fav_articles:
                article_dict = fav_article.article.to_dict()
                article_dict['is_favorite'] = True
                articles_dict.append(article_dict)
            
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
                article_dict = article.to_dict()
                if FavoriteArticle.objects.filter(user=user_id, article=article.id).count() > 0:
                    article_dict['is_favorite'] = True
                else:
                    article_dict['is_favorite'] = False
                    
                return JsonResponse({'result': 'ok', 'article': article_dict})

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


@csrf_exempt
def get_article_types(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']
        
        if check_user2(token, user_id):
            article_types = ArticleType.objects.all()
            
            article_types_dict = []
            
            for article_type in article_types:
                article_types_dict.append(article_type.to_dict())
            
            return JsonResponse({'result': 'ok', 'article_types': article_types_dict})
        
        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def read_article(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']
        article_id = data['article_id']

        if check_user2(token, user_id):
            article = get_object_or_None(Article, id=article_id)

            if not article:
                return JsonResponse({'result': 'error', 'message': 'Artículo no encontrado'})
            
            user_extra_data = get_object_or_None(UserExtraData, user__id=user_id)
            if not user_extra_data:
                user_extra_data = UserExtraData(user=get_object_or_None(User, id=user_id))
                user_extra_data.save()

            if str(article.id) not in user_extra_data.read_articles:
                user_extra_data.read_articles.append(article_id)
                user_extra_data.save()

            return JsonResponse({'result': 'ok', 'message': 'Artículo leído'})
        
        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def get_recommended_articles(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']

        if check_user2(token, user_id):
            user_extra_data = get_object_or_None(UserExtraData, user__id=user_id)
            if not user_extra_data:
                user_extra_data = UserExtraData(user=get_object_or_None(User, id=user_id))
                user_extra_data.save()

            read_articles = user_extra_data.read_articles
            
            articles = Article.objects.filter(recommend=True)

            articles_list = []

            for article in articles:
                if str(article.id) not in read_articles:
                    article_dict = article.to_dict()
                    if FavoriteArticle.objects.filter(user=user_id, article=article.id).count() > 0:
                        article_dict['is_favorite'] = True
                    else:
                        article_dict['is_favorite'] = False

                    articles_list.append(article_dict)
                
                if len(articles_list) == 10:
                    break

            return JsonResponse({'result': 'ok', 'articles': articles_list})

        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})

    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})


@csrf_exempt
def send_article_comment(request):
    try:
        data = json.loads(request.POST['data'])
        token = data['token']
        user_id = data['user_id']
        article_id = data['article_id']
        comment_text = data['comment_text']
    
        if check_user2(token, user_id):
            article = get_object_or_None(Article, id=article_id)
            user = get_object_or_None(User, id=user_id)
            
            if article and user:
                comment = ArticleComment(article=article, user=user, text=comment_text)
                comment.save()
                
                return JsonResponse({'result': 'ok', 'message': 'Comentario enviado'})
            
            return JsonResponse({'result': 'error', 'message': 'Artículo o usuario no encontrado'})

        return JsonResponse({'result': 'error', 'message': 'Usuario no autorizado'})
    
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)})
    
    