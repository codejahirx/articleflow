from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = slug = AutoSlugField(
        populate_from='title', unique=True, null=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category', args=[str(self.slug)])


class Post(models.Model):
    option = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = slug = AutoSlugField(
        populate_from='title', unique=True, null=True, default=None)
    content = models.TextField()
    images = models.ImageField(upload_to='images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pub_status = models.CharField(
        max_length=10, choices=option, default='draft')
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.slug)])


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
