from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views import View
from .models import State
from country.models import Country
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
class StatePageView(View):
    def get(self,request):
        query = self.request.GET.get('search')
        country_serach = self.request.GET.get('country_search')
        print(country_serach,"fjkjnfgn")
      
        if query:
             states = State.objects.filter(name__icontains=query,is_deleted=False)
        elif country_serach: 
            states = State.objects.filter(country__id__icontains=country_serach,is_deleted=False)
            print(states)
         
        else:
            states = State.objects.filter(is_deleted=False)
        countries=Country.objects.filter(is_deleted=False)
        
        return render(request,'state/home.html',locals())
    def post(self,request):
        state_name = request.POST.get('name')
        state_code = request.POST.get('code')
        selected_item = (request.POST.get('item_id'))
        country_name  = Country.objects.get(id=selected_item)
        data=State(name=state_name,code=state_code,country=country_name)
        print(data,"get")
        try:
            if state_name and state_code and country_name:

                data.save()
                messages.success(request, 'Created!!')
            else:
                messages.warning(request, 'enter name ,code and country name!!!')

        except:
             messages.warning(request, 'Alreday exits')
        return redirect('state:state_home')
@class_view_decorator(login_required)          
class StateDeleteView(View):
    def get(self,request,id):
        state_detail = State.objects.get(pk=id)
        print(state_detail,"hi")
        state_detail.is_deleted=True
        state_detail.save()
        messages.warning(request, 'Successfully Deleted')
        return HttpResponseRedirect('/state/state_home/')
@class_view_decorator(login_required)          
class StateEditView(View):
    def get(self,request,id):
        state_detail = State.objects.get(pk=id)
        print(state_detail,"hi")
        return render(request,'state/edit.html',{'state_detail':state_detail})
    def post(self,request,id):
        state_name = request.POST.get('name')
        state_code = request.POST.get('code')

        state_detail = State.objects.get(pk=id)
        
        state_detail.name = state_name
        state_detail.code = state_code
        state_detail.save()
        return redirect('state:state_home')
@class_view_decorator(login_required)          
class StateDeltailView(View):
    def get(self,request,id):
        state_detail = State.objects.get(pk=id)
        print(state_detail,"hi")
        return render(request,'state/details.html',{'state_detail':state_detail})
