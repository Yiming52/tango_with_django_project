from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)  # 允许上传图片

    def __str__(self):
        return self.name
