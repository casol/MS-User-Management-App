from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('home/', views.home, name='home'),
    path('user/<username>/', views.user_details, name='user_details'),
    path('users/', views.user_list, name='user_list'),

    path('signup/', views.signup, name='signup'),
    path('edit/', views.user_edit, name='user_edit'),
    path('delete/', views.user_delete, name='user_delete'),
    path('download/', views.export_user_csv, name='export_user_csv'),

]
