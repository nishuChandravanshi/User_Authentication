from django.db import models
from django.contrib.auth.models import User #this is the builtin user--present in admin page

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    #additional
    portfolio_site= models.URLField(blank=True)

    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)
    # ie the uploaded images will be saved under 'profile_pics' in media folder

    def __str__(self):
        return self.user.username
