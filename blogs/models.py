from PIL import Image
from django.db import models

from accounts.models import User


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)


class Blog(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=150)
    banner = models.ImageField()
    description = models.TextField()
    total_views = models.IntegerField(default=0)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blogs')

    REQUIRED_FIELDS = ['category', 'title', 'banner', 'description']

    def save(self, *args, **kwargs):
        img = Image.open(self.banner)
        quality = 60  # 60% of original quality
        img.save(self.banner.path, quality=quality)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title}'


class Post(models.Model):
    title = models.CharField(max_length=255)
    post_text = models.TextField()
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
