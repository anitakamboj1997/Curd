from django.contrib import admin
from django.urls import path
from .views import HomePageView,DeltailView,EditView,DeleteView


app_name='country'
urlpatterns = [
    path('country_home/', HomePageView.as_view(),name='country_home'),
    path('detail/<int:id>/',DeltailView.as_view(), name='detail'),
    path('edit_detail/<int:id>/',EditView.as_view(), name='edit_detail'),
    path('delete_country/<int:id>/', DeleteView.as_view(), name='delete_country')
]
