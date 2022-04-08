from django.urls import path
from .views import Signup,Login,Logout
from .views import AddCountry,GetCountries,GetCountryDetail,EditCountryDetail,DeleteCountry
from .views import AddState,DeleteState,GetStates,GetStateDetail,EditState
from .views import AddCity,DeleteCity,EditCity

urlpatterns = [
    path('signup/',Signup.as_view(), name='auth-signup'),
    path('login/', Login.as_view(), name='auth-login'),
    path('logout/', Logout.as_view(), name='auth-logout'),
    path('add_country/', AddCountry.as_view(), name='auth-add_country'),
    path('get_countries/', GetCountries.as_view(), name='auth-get_countries'),
    path('get_countries_details/<int:nm>/', GetCountryDetail.as_view(), name='auth-get_countries_details'),
    path('edit_countries_details/<int:nm>/', EditCountryDetail.as_view(), name='auth-edit_countries_details'),
    path('delete_country/<int:nm>/', DeleteCountry.as_view(), name='auth-delete_country'),

    path('add_state/', AddState.as_view(), name='auth-add_state'),
    path('delete_state/<int:nm>/', DeleteState.as_view(), name='auth-delete_state'),
    path('get_states/', GetStates.as_view(), name='auth-get_states'),
    path('get_state_details/<int:nm>/', GetStateDetail.as_view(), name='auth-get_state_details'),
    path('edit_state_details/<int:nm>/', EditState.as_view(), name='auth-edit_state_details'),

    path('add_city/', AddCity.as_view(), name='auth-add_city'),
    path('delete_city/<int:nm>/', DeleteCity.as_view(), name='auth-delete_city'),
    path('edit_city_details/<int:nm>/', EditCity.as_view(), name='auth-edit_city_details'),




]