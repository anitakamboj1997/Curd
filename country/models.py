from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(unique=True,max_length=100,)
    code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,related_name='created_by',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User,related_name='updated_by',on_delete=models.CASCADE,blank=True,null=True)

