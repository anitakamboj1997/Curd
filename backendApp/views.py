from datetime import date
from email import message
from multiprocessing import context
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from rest_framework.authentication import TokenAuthentication
import json

from city.models import City


from .serializers import GetCountrySerializer, SignupSerializer, LoginSerializer
from .serializers import AddCountrySerializer,GetCountryDetailSerializer,EditCountrySerializer,DeleteCountrySerializer
from .serializers import AddStateSerializer,DeleteStateSerializer,GetStateSerializer,GetStateDetailSerializer,EditStateSerializer
from .serializers import AddCitySerializer,DeleteCitySerializer,EditCitySerializer
import random
from country.models import Country
from state.models import State
from rest_framework.fields import CurrentUserDefault
from django.core import serializers



def create_username(first_name,last_name):
        first_name = first_name[:4]
        last_name = last_name[:4]
        n = str(random.randint(1,30))
        username=str(first_name+last_name+n)
        return(username) 
class Signup(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']
            username = create_username(first_name,last_name)
            if User.objects.filter(email=email).exists():
                content = {'detail':
                           _('Email exists')}
                return Response(content, status=status.HTTP_201_CREATED)
            elif User.objects.filter(username=username).exists():
                content = {'detail':
                           _('Username exits')}
                return Response(content, status=status.HTTP_201_CREATED)    
           
            else:       
                user=User(first_name=first_name,last_name=last_name,username=username,email=email)
                user.set_password(password)
                user.save()
                content = {'email': email, 'first_name': first_name,
                        'last_name': last_name,'user_name=':username}
                return Response(content, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user:
                    token,created = Token.objects.get_or_create(user=user)
                    print(type(token))
                    content={'token': token.key,'user':user.username,'email':user.email,'password':password}
                    return Response(content,status=status.HTTP_200_OK)
            else:
                content = {'detail':
                           _('Unable to login with provided credentials.')}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
                       
class Logout(APIView):
    
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        """
        Remove all auth tokens owned by request.user.
        """
        tokens = Token.objects.filter(user=request.user)
        for token in tokens:
            token.delete()
        content = {'success': _('User logged out.')}
        return Response(content, status=status.HTTP_200_OK)
class AddCountry(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = AddCountrySerializer
    def post(self, request, format=None):
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    name = serializer.data['name']
                    code = serializer.data['code']
                    if Country.objects.filter(name=name).exists():
                        content = {'detail':
                                _('Name already exists')}
                    else:       
                        country=Country(name=name,code=code,created_by = request.user)
                        country.save()
                        created_by=str(request.user)
                        print(created_by)
                        content = {'name': name, 'code': code ,'created_by':created_by }
                    return Response(content, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCountries(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = AddCountrySerializer
    def get(self, request, format=None):
            countries = list(Country.objects.filter(is_deleted=False).values('name','code','created_by','updated_by'))
            
            
            return Response(countries,status=status.HTTP_200_OK )
                

class GetCountryDetail(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = GetCountryDetailSerializer
    def get(self, request, nm):
            country_detail = Country.objects.get(id=nm,is_deleted=False)
            if country_detail:
                context={'status':True,'name':country_detail.name,'code':country_detail.code,'created_by':country_detail.created_by.username}
                return Response(context, )
            else:    
                content = {'message':"No Record" }
                return Response(content,status=201)
                     
class EditCountryDetail(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = EditCountrySerializer

    def post(self, request, nm):
            print("hi")
            serializer = self.serializer_class(data=request.data)
            try:
                if serializer.is_valid():
                        name = serializer.data['name']
                        print(type(name))
                        code = serializer.data['code']
                        country = Country.objects.get(id=nm)
                        country.code = code
                        country.save()
                        status= True
                        content = {'name': name, 'code': code ,'status':status ,'message':'updated'}
                        return Response(content)
            except:
                content = {'message':"Something worng" }
                return Response(content,status=201)

            else:        

                return Response(serializer.errors,status=status.HTTP_200_OK)


class DeleteCountry(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = DeleteCountrySerializer
    def post(self, request, nm):
            print("hi")
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                try:
                    country = Country.objects.get(id=nm)
                    if country:
                        country.is_deleted = True
                        country.save()
                        status= True
                        content = { 'message':'Delete Succesfully'}
                        return Response(content)
                except:        
                    content = { 'message':'Something worng!!!'}
                    return Response(content)
            else:  
                return Response(serializer.errors,status=status.HTTP_200_OK)
                
class AddState(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = AddStateSerializer
    def post(self, request, format=None):
                print("hi ")
                serializer = self.serializer_class(data=request.data)
                print(serializer)
                if serializer.is_valid():
                    name = serializer.data['name']
                    code = serializer.data['code']
                    country_id=serializer.data['country']
                   

                    if State.objects.filter(name=name).exists():
                        content = {'detail':
                                _('Name already exists')}
                        return Response(content, status=status.HTTP_201_CREATED)
                   
                    else:       
                        country=Country.objects.get(id=country_id)
                        print(country)
                        if country:
                           
                            state=State(name=name,code=code,created_by = request.user,country=country)
                            state.save()
                            created_by=str(request.user)
                            country=(country.name)
                            country=str(country)
                            print(created_by)
                            content = {'name': name, 'code': code ,'created_by':created_by,'country':country }
                            return Response(content, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteState(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = DeleteStateSerializer
    def post(self, request, nm):
            print("hi")
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    country = State.objects.get(id=nm)
                    country.is_deleted = True
                    country.save()
                    status= True
                    content = { 'message':'Delete Succesfully'}
                    return Response(content)
                except:
                    content = { 'message':'Something wrong'}
                    return Response(content)

            else:  
                return Response(serializer.errors,status=status.HTTP_200_OK)
class GetStates(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = GetStateSerializer
    def get(self, request, format=None):
            states = State.objects.filter(is_deleted=False)
            if states:
                data=self.serializer_class(states,many=True)
                states=data.data
                content = {'status':True,'data': states, 'message':"Country Record" }
                return Response(content,status=200 )
            else:    
                content = {'message':"No Record" }
                return Response(content,status=201)
                   
class GetStateDetail(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = GetStateDetailSerializer
    def get(self, request, nm):
            state = State.objects.filter(id=nm,is_deleted=False)
            if state:
                print(state)
                data=serializers.serialize("json",state)
                data = json.loads(data)
                content = {'data':data}
                return Response(content, status=status.HTTP_200_OK)
            else:    
                content = {'message':"No Record" }
                return Response(content,status=201)
class EditState(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = EditStateSerializer

    def post(self, request, nm):
            print("hi")
            serializer = self.serializer_class(data=request.data)
            
            if serializer.is_valid():
                try:
                        name = serializer.data['name']
                        print(type(name))
                        code = serializer.data['code']
                        state = State.objects.get(id=nm)
                        state.name=name
                        state.code = code
                        state.save()
                        status= True
                        content = {'name': name, 'code': code ,'status':status ,'message':'updated'}
                        return Response(content)
                except:
                     content = {'message':"Something worng" }
                     return Response(content,status=201)


            else:        

                return Response(serializer.errors,status=status.HTTP_200_OK)

class AddCity(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = AddCitySerializer
    def post(self, request, format=None):
                print("hi ")
                serializer = self.serializer_class(data=request.data)
                print(serializer)
                if serializer.is_valid():
                    print("jbvv")
                    name = serializer.data['name']
                    code = serializer.data['code']
                    state_id=serializer.data['state']
                    print(state_id)
                    if City.objects.filter(name=name).exists():
                        content = {'detail':
                                _('Name already exists')}
                        return Response(content, status=status.HTTP_201_CREATED)
                   
                    else:       
                        state=State.objects.get(id=state_id)
                        print(state)
                        
                        if state:
                            city=City(name=name,code=code,created_by = request.user,state=state)
                            city.save()
                            created_by=str(request.user)
                            state=(state.name)
                            state=str(state)
                            print(created_by)
                            content = {'name': name, 'code': code ,'created_by':created_by,'state':state }
                            return Response(content, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteCity(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = DeleteCitySerializer
    def post(self, request, nm):
            print("hi")
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    city = City.objects.get(id=nm , is_deleted=False)
                    if city:
                        city.is_deleted = True
                        city.save()
                        status= True
                        content = { 'message':'Delete Succesfully'}
                        return Response(content)
                except:
                        content = { 'message':'no record'}
                        return Response(content)
            else:  
                return Response(serializer.errors,status=status.HTTP_200_OK)
class EditCity(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = EditCitySerializer

    def post(self, request, nm):
            print("hi")
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    name = serializer.data['name']
                    print(type(name))
                    code = serializer.data['code']
                    city = City.objects.get(id=nm)
                    city.name = name
                    city.code = code
                    city.save()
                    status= True
                    content = {'name': name, 'code': code ,'status':status ,'message':'updated'}
                    return Response(content)
                except:    
                    content = {'message':"Something worng" }
                    return Response(content,status=201)

            else:        

                return Response(serializer.errors,status=status.HTTP_200_OK)                