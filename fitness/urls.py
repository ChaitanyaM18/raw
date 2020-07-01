from django.urls import path
from fitness.views import HomeView,AddUsersCreate

urlpatterns = [
    path('', HomeView.as_view(),name='home'),
    path('add/',AddUsersCreate.as_view(),name='add'),
]