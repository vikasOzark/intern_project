from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# import slugify
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField

# Create your models here.
class UserProfileModel(models.Model):
    user = models.OneToOneField(User,related_name="usr_persion", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media', blank=True)
    address = models.CharField(max_length=200, blank=True)
    is_patient = models.BooleanField(default=True)


    def __str__(self):
        return self.user.username


choices = [
    ('MH' , 'Mental health'),
    ('C19' , 'Covid19'),
    ('HD' , 'Heart Disease'),
    ('IM' , 'Immunization'),   

]
    
class BlogModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(max_length=200, unique=True, populate_from='title', editable=True)
    summary = models.CharField(max_length=200)
    blog_image = models.ImageField(upload_to='media', blank=True)
    content = models.TextField()
    modified_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    MENTALHEALTH = 'MH'
    COVID19 = 'C19'
    HEARTDISEASE = 'HD'
    IMMUNIZATION = 'IM'
    choices = [
        (MENTALHEALTH , 'Mental health'),
        (COVID19 , 'Covid19'),
        (HEARTDISEASE , 'Heart Disease'),
        (IMMUNIZATION , 'Immunization'),
    ]
    category = models.CharField(max_length=200, choices=choices)

    
    def __str__(self):
        return f'{self.title} -> {self.user}' 
    
    def get_absolute_url(self):
        return reverse("blog_view", kwargs={"slug": self.slug})
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class BookAppointment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appoint')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appoint')
    # profile = models.OneToOneField(UserProfileModel, on_delete)
    apppoint_date = models.DateField()
    appoint_time = models.TimeField()
    discription = models.TextField()
    is_pending = models.BooleanField(default=True)

    def __str__(self): 
        return f'{self.patient} -> {self.doctor}'
