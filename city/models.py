from django.db import models
from state.models import State
from django.contrib.auth.models import User

class City(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,related_name='city_created_by',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User,related_name='city_updated_by',on_delete=models.CASCADE,blank=True,null=True)


