from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from city.models import City

from country.models import Country
from state.models import State

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
class SignupSerializer(serializers.Serializer):
   
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)
    first_name = serializers.CharField(max_length=30, default='',
                                       required=False)
    last_name = serializers.CharField(max_length=30, default='',
                                      required=False)
    
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)
    class Meta:
        model = User
        fields = '__all__'



class AddCountrySerializer(serializers.ModelSerializer):
    created_by = serializers.RelatedField(source='User', read_only=True)
    class Meta:
        model = Country
        fields = '__all__'    
class GetCountrySerializer(serializers.ModelSerializer):
     created_by = serializers.RelatedField(queryset=User.objects.all())

    
     class Meta:
        model = Country
        fields = ['id','name','code','created_by']              
class GetCountryDetailSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
  
    class Meta:
        model = Country
        fields = ['id','name','code','created_by']                   
class EditCountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = ['name','code' ]                         
class DeleteCountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = ['id']  
class AddStateSerializer(serializers.ModelSerializer):
    created_by = serializers.RelatedField(source='User.username',read_only=True)
    print(created_by)
    class Meta:
        model = State
        fields = ['name','code','country','created_by']         
class DeleteStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id']  
class GetStateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = State
        fields = '__all__'         
class GetStateDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = State
        fields = '__all__'         
class EditStateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = State
        fields = ['name','code' ]           
class AddCitySerializer(serializers.ModelSerializer):
    created_by = serializers.RelatedField(source='User', read_only=True)
    class Meta:
        model = City
        fields = ['name','code','state','created_by']         
class DeleteCitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = City
        fields = ['id']  
class EditCitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = City
        fields = ['name','code' ]          
