from django.urls import path, include
from users import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.UsersListView.as_view(), name='users'),
    path('create/', views.RegisterUserView.as_view(), name='register'),
    path('<int:pk>/update/', views.UpdateUserView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete'),
]
