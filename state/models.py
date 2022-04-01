from django.db import models
from country.models import Country

class State(models.Model):
    country=models.ForeignKey(Country,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code=models.CharField(max_length=20,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(blank=True, null=True)
    is_deleted=models.BooleanField(default=False)
