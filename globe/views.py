from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import logout

def HomeView(request):
       
        return render(request,'base.html',locals())