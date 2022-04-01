import email
from errno import EALREADY
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views import View
import random
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login


def create_username(first_name,last_name):
        first_name = first_name[:4]
        last_name = last_name[:4]
        n = str(random.randint(1,30))
        username=str(first_name+last_name+n)
        return(username)  

class SignUpView(View):
    def get(self,request):
        users = User.objects.all()
        print(users,"0000000000000000")
        return render(request,'login_Signup/signup.html')
      
    def post(self,request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        password_repeat=request.POST.get('password_repeat')
        username = create_username(first_name,last_name)
        if User.objects.filter(email=email_address).exists():
            messages.warning(request, 'Email aready exits')
            return HttpResponseRedirect('/users/')
        elif password == password_repeat:
            data = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email_address,password=make_password(password))
            data.save()
            messages.success(request, username,'Succesfully Login ')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'something wrong!!')
            return HttpResponseRedirect('/users/')
class LoginView(View):
    def get(self,request):
        return render(request,'login_Signup/login.html')
    def post(self,request):
        email_address = request.POST.get('email_address')
        print(email_address)
        password = request.POST.get('password')
        print(password)
        try:
            user = User.objects.get(email=email_address)
            username = user.username
            user = authenticate(username=username, password=password)
            print(user,"dkfndngnj")
            if user is not None:
                login(request, user)
                print('yes')
                
                return HttpResponseRedirect('/')
            else:
                 messages.warning(request, 'something wrong!!')
                 return HttpResponseRedirect('/')
        except User.DoesNotExist:
            
            messages.warning(request, 'something wrong!!')
            return HttpResponseRedirect('/')
      
       
   
class LogoutView(View):
     def get(self,request):
        if request.user.is_authenticated:
            logout(request) 
        else:
            print("User is not logged in :(")

        return redirect('/users/login/')
     
          