from django.urls import path

from users import views


urlpatterns = [
    path('', views.UsersListView.as_view(), name='users_list'),
    path('create/', views.RegisterUserView.as_view(), name='register'),
    path('<int:pk>/update/', views.UpdateUserView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete'),
]
