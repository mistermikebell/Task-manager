from django.urls import path, include
from task_manager.users import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.UsersList.as_view(), name='users'),
    path('create/', views.RegisterUser.as_view(), name='register'),
    path('<int:pk>/update/', views.UpdateUser.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteUser.as_view(), name='delete'),
]
