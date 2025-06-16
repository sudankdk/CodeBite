from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class MyUser(AbstractUser):
    email = models.EmailField()
    is_verified= models.BooleanField(default=False) # ya email verification aauxa
    esewa_id=models.CharField(max_length=200,blank=True,null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering= ['username']
        
    def __str__(self):
        return self.username
    
class Skills(models.Model):
    name= models.CharField(max_length=100, unique=True)
    slug= models.SlugField(max_length=200, unique=True,blank=True)
    created_at= models.DateTimeField(auto_now=False, auto_now_add=True)
    
    class Meta:
        ordering=['name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Profile(models.Model):
    user= models.OneToOneField(MyUser,on_delete=models.CASCADE,related_name="Profile")
    bio=models.TextField(max_length=500,blank=True)
    skills_offered=models.ManyToManyField(Skills,blank=True,related_name="offered_skills")
    skills_sought=models.ManyToManyField(Skills,blank=True,related_name="sought_skills")
    average_rating = models.FloatField(default=0.0)  
    review_count = models.PositiveIntegerField(default=0) 
    profile_image = models.URLField(max_length=500, blank=True, null=True) 
    location = models.CharField(max_length=100, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}"
    
    class Meta:
        ordering=["created_at"]
        
    def update_rating(self,new_rating):
        self.review_count +=1
        self.average_rating = ((self.average_rating * (self.review_count - 1)) + new_rating) / self.review_count
        self.save()
 