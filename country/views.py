
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views import View
from .models import Country
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def class_view_decorator(function_decorator):
    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


@class_view_decorator(login_required)    
class HomePageView(View):
    def get(self,request):
        countries = Country.objects.filter(is_deleted=False)
        query = self.request.GET.get('search')
        print(query)
        if query:
             countries = Country.objects.filter(name__icontains=query,is_deleted=False)
        else:
             countries = Country.objects.filter(is_deleted=False)
        return render(request,'country/home.html',locals())
        
    def post(self,request):
        country_name = request.POST.get('name')
        print(country_name)
        country_code = request.POST.get('code')
        created_by=request.user
        print(created_by)
        data = Country(name=country_name,code=country_code,created_by=created_by)
        print(data,"sdksdksdsldls")
        try:
            if country_name and country_code:
                    data.save()
                    messages.success(request, 'Created!!')
            else:
                messages.warning(request, 'enter name and code!!!')
        except:
             messages.warning(request, 'Alreday exits')
            
        return redirect('country:country_home')


@class_view_decorator(login_required)
class DeltailView(View):
    def get(self,request,id):
        Country_detail = Country.objects.get(pk=id)
        print(Country_detail,"hi")
        return render(request,'country/details.html',locals())


@class_view_decorator(login_required)        
class EditView(View):
    def get(self,request,id):
        Country_detail = Country.objects.get(pk=id)
        print(Country_detail,"hi")
        return render(request,'country/edit.html',locals())
    def post(self,request,id):
        country_name = request.POST.get('name')
        country_code = request.POST.get('code')
        Country_detail = Country.objects.get(pk=id)
        Country_detail.name = country_name
        Country_detail.code = country_code
        Country_detail.save()
        return redirect('country:country_home')

@class_view_decorator(login_required)
class DeleteView(View):
    def get(self,request,id):
        Country_detail = Country.objects.get(pk=id)
        print(Country_detail,"hi")
        Country_detail.is_deleted = True
        Country_detail.save()
        messages.warning(request, 'Successfully Deleted')
        return redirect('country:country_home')

        