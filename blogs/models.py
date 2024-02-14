from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)


class Blog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='blogs')
    title = models.CharField(max_length=150)
    banner = models.ImageField()
    details = models.TextField()
    total_views = models.IntegerField(default=0)

    REQUIRED_FIELDS = ['category', 'title', 'banner', 'details']

    def __str__(self) -> str:
        return f'{self.title} - ({self.category})'


class Post(models.Model):
    title = models.CharField(max_length=255)
    post_text = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, related_name='posts')
