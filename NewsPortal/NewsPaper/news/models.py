from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user_relation = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += post_rating.get('postRating')

        comment_rating = self.user_relation.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += comment_rating.get('commentRating')

        self.rating = pRat*3 + cRat
        self.save()


class Category(models.Model):
    article_theme = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author_relation = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_TYPE = (
        (NEWS, 'Новость'),
        (ARTICLE, 'AR')
    )
    type = models.CharField(max_length=2, choices=CATEGORY_TYPE, default=ARTICLE)
    datetime = models.DateTimeField(auto_now_add=True)
    category_relation = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    post_relation = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_relation = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_relation = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_relation = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
