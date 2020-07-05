from django.urls import path
from .import views

urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('add/',views.AddUsersCreate.as_view(),name='add'),
    path('list/',views.UsersListView.as_view(),name='list'),
    path('update/<int:pk>',views.UsersUpdateView.as_view(),name='update'),
    path('delete/<int:pk>',views.UsersDeleteView.as_view(),name='delete'),
    path('get_alerts',views.get_alerts,name='get_alerts'),
    path('generate_invoice/',views.generate_invoice,name='generate_invoice'),
]
