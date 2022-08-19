from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class UserProfileModel(models.Model):
    user = models.OneToOneField(User,related_name="usr_persion", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media', blank=True)
    address = models.CharField(max_length=200, blank=True)
    is_patient = models.BooleanField(default=True)


    def __str__(self):
        return self.user.username

# class AssignedDoctor(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(User, on_delete=models.CASCADE)


#     def __str__(self):
#         return self.user.username
