# from django.urls import path
# from home import views

# urlpatterns = [
#     path('', views.index, name = 'home'),
#     # path("os" , views.os , name='os'),
#     path("system_info/", views.system_info, name='system_info'),
#     path("index/", views.system_info_ui, name='system_info_ui'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Route for the login endpoint
    # path('index/', views.index, name='index'),  # Route for the home page
    path('summary/', views.summary, name='summary'), 
    path('summary/os/', views.os, name='os'), 
    path('summary/cpu/', views.cpu, name='cpu'), 
    path('system_info/', views.system_info, name='system_info'),  # Route for the system info endpoint
]