from django.contrib import admin
from django.urls import path, include
from task_manager import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('statuses/', include('statuses.urls')),
    path('statuses/', include('django.contrib.auth.urls')),
    path('tasks/', include('tasks.urls')),
    path('labels/', include('labels.urls')),
]
