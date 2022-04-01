from django.shortcuts import redirect, render,HttpResponseRedirect
from django.views import View
from state.models import State
from country.models import Country
from .models import City
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator
@class_view_decorator(login_required) 
class CityPageView(View):
    def get(self,request):
        states = State.objects.filter(is_deleted=False)
        countries=Country.objects.filter(is_deleted=False)
        query = self.request.GET.get('search')
        state_serach = self.request.GET.get('state_search')
        country_search=self.request.GET.get('country_search')
        print(country_search)
        print(state_serach,"fjkjnfgn")
        if query:
             cities = City.objects.filter(name__icontains=query,is_deleted=False)
             print(cities)
        elif state_serach:
            cities = City.objects.filter(state__id__icontains=state_serach,is_deleted=False)
        elif country_search:

            cities = City.objects.filter(state__country__id__icontains=country_search,is_deleted=False)
           
        else:     
             cities = City.objects.filter(is_deleted=False)
        return render(request,'city/home.html',locals())
    def post(self,request):
            city_name = request.POST.get('name')
            city_code = request.POST.get('code')
            selected_state = (request.POST.get('state_id'))
          
            state_name  = State.objects.get(id=selected_state)
            print(state_name,"fddfsdbhdjbvjdf")
            data=City(name=city_name,code=city_code,state=state_name)
            print(data,"get")
            try:
                if state_name and city_name and city_code:

                    data.save()
                    messages.success(request, 'Created!!')
                else:
                    messages.warning(request, 'enter name ,code and country name!!!')

            except:
                messages.warning(request, 'Alreday exits')
            return redirect('city:city_home')
@class_view_decorator(login_required) 
class CityDeltailView(View):
    def get(self,request,id):
        city_detail = City.objects.get(pk=id)
        print(city_detail,"hi")
        return render(request,'city/details.html',{'city_detail':city_detail})
@class_view_decorator(login_required)         
class CityEditView(View):
    def get(self,request,id):
        city_detail = City.objects.get(pk=id)
        print(city_detail,"hi")
        return render(request,'city/edit.html',{'city_detail':city_detail})
    def post(self,request,id):
        city_name = request.POST.get('name')
        city_code = request.POST.get('code')
        city_detail = City.objects.get(pk=id)
        city_detail.name=city_name
        city_detail.code=city_code
        city_detail.save()
        return redirect('city:city_home')
@class_view_decorator(login_required)         
class CityDeleteView(View):
    def get(self,request,id):
        city_detail = City.objects.get(pk=id)
        print(city_detail,"hi")
        city_detail.is_deleted=True
        city_detail.save()
        messages.warning(request, 'Successfully Deleted')
        return redirect('city:city_home')        