from django.contrib import admin
from django.urls import path, include
from task_manager import views
from users import views as users_views

urlpatterns = [
    path('', views.MyTasksListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('statuses/', include('statuses.urls')),
    path('tasks/', include('tasks.urls')),
    path('labels/', include('labels.urls')),
    path('login/', users_views.LoginUserView.as_view(), name='login'),
    path('logout/', users_views.LogoutUserView.as_view(), name='logout'),
]
