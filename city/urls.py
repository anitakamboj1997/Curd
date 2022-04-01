from django.contrib import admin
from django.urls import path
from .views import CityPageView,CityDeltailView,CityEditView,CityDeleteView
app_name='city'
urlpatterns = [
    path('city_home/', CityPageView.as_view(),name='city_home'),
    path('city_detail/<int:id>/',CityDeltailView.as_view(), name='city_detail'),
    path('edit_city_details/<int:id>/',CityEditView.as_view(), name='edit_city_details'),
    path('delete_city/<int:id>/', CityDeleteView.as_view(), name='delete_city'),


]