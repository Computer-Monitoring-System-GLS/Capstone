# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.login_view, name='login'),  # Route for the login endpoint
#     # path('index/', views.index, name='index'),  # Route for the home page
#     path('summary/', views.summary, name='summary'), 
#     path('summary/os/', views.os, name='os'), 
#     path('summary/cpu/', views.cpu, name='cpu'), 
#     path('summary/motherboard/', views.motherboard, name='motherboard'),
#     path('summary/gpu/', views.gpu, name='gpu'),
#     path('summary/ram/', views.ram, name='ram'),
#     path('summary/storage/', views.storage, name='storage'),
#     path('summary/audio/', views.audio, name='audio'),
#     path('summary/network/', views.network, name='network'),
#     path('summary/peripherals/', views.peripherals, name='peripherals'),
#     path('summary/software/', views.software, name='software'),
#     path('system_info/', views.system_info, name='system_info'), 
# ]




from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Login page
    path("devices/", views.device_list, name="device_list"),  # List available devices
    path('device/<str:ip>/json/', views.fetch_remote_device_info, name='fetch_remote_device_info'),
    path("device/<str:ip>/summary/", views.device_summary, name="device_summary"),  # Fetch remote device info
    path('summary/', views.summary, name='summary'),

    # System summary and category-specific endpoints
    path('summary/os/', views.os_info, name='os'),
    path('summary/cpu/', views.cpu, name='cpu'),
    path('summary/motherboard/', views.motherboard, name='motherboard'),
    path('summary/gpu/', views.gpu, name='gpu'),
    path('summary/ram/', views.ram, name='ram'),
    path('summary/storage/', views.storage, name='storage'),
    path('summary/audio/', views.audio, name='audio'),
    path('summary/network/', views.network, name='network'),
    path('summary/peripherals/', views.peripherals, name='peripherals'),
    path('summary/software/', views.software, name='software'),
    path('system_info/', views.system_info, name='system_info'),

    # Fix the incorrect line (this should fetch the correct client data)
    path("device/<str:ip>/", views.device_summary, name="view_device_data"),

    # This ensures that each client only sees **their** saved data
    path("my-device/", views.view_client_data, name="view_client_data"),
    # path("device/<str:ip>/", views.view_client_data, name="view_client_data_by_ip"),
]
