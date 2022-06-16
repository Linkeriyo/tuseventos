from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='static/articles')
    date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField()
    lng = models.FloatField()
    article_type = models.ForeignKey('ArticleType', on_delete=models.CASCADE)
    recommend = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'text': self.text,
            'image': self.image.url if self.image else None,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'lat': self.lat,
            'lng': self.lng,
            'article_type': self.article_type.to_dict(),
            'recommend': self.recommend,
        }


class FavoriteArticle(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.article.title

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'article': self.article.title
        }


class ArticleType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
