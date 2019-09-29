from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import User




def generate_filename(instance, filename):
    filename = instance.slug + '.jpg'
    return "{0}/{1}".format(instance, filename)


class Category(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField()

    image = models.ImageField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})


class Course(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    image = models.ImageField()
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    objects = models.Manager()
    comments = GenericRelation('comments')



    def __str__(self):
        return "'{0}''{1}'".format(self.title, self.category.name)



    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'category': self.category.slug, 'slug': self.slug})


class Comments(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')



class UserAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    favourite_courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('account_view', kwargs={'user':self.user.username})


