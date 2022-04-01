from django.db import models


class Country(models.Model):
    name = models.CharField(unique=True,max_length=100)
    code=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)

