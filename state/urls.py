from django.contrib import admin
from django.urls import path
from .views import StatePageView,StateDeleteView,StateEditView,StateDeltailView

app_name='state'

urlpatterns = [
    path('state_home/', StatePageView.as_view(),name='state_home'),
    path('delete_state/<int:id>/', StateDeleteView.as_view(), name='delete_state'),
    path('edit_state_details/<int:id>/',StateEditView.as_view(), name='edit_state_details'),
    path('state_detail/<int:id>/',StateDeltailView.as_view(), name='state_detail'),
]
# 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