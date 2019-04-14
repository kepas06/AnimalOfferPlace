from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null= True, related_name='children', on_delete=models.CASCADE)
  
    class Meta:
        unique_together = ('slug', 'parent',)   
        verbose_name_plural = "categories"        
                                                  
    def __str__(self):                           
        full_path = [self.name]                  
                                                 
        k = self.parent                          

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=False)
    price = models.IntegerField()
    contact = models.IntegerField()
    photo = models.ImageField(upload_to='offer_images/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', null=True, blank=True,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, db_index=True,default="None")
    is_published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('offers:offer_detail',args=[self.title, self.slug])

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
        
    def __str__(self):
        return self.title


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=False)
    category = models.ForeignKey('Category', null=True, blank=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def get_absolute_url(self):
        return reverse('questions:question_detail',args=[self.title])


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    #country = CountryField(blank_label='(select country)')
    contact = models.IntegerField()
    offers = models.ForeignKey(Offer, on_delete=models.CASCADE)
