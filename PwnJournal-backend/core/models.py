from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    # Inherit all fields from AbstractUser


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(_("fullname"), max_length=50)
    contact = models.CharField(_("phone_number"), max_length=20)
    DP = models.ImageField(_("profile_picture"), upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Writeup(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=100)
    contents = models.TextField()
    post = models.DateTimeField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    keywords = models.TextField(blank=True, default='[]')  
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    author =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comments(models.Model):
    content= models.CharField(max_length=200)
    posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    onwriteup = models.ForeignKey(Writeup, on_delete=models.CASCADE)

    def __str__(self):
        return f''+self.author.username+' on '+ self.onwriteup.title

class likes(models.Model):
    post= models.ForeignKey(Writeup,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,models.CASCADE)