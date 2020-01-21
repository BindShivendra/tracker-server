from django.urls import path

from . import views


urlpatterns = [
    path('', views.UserListView.as_view()),
    path('register', views.UserRegisterView.as_view()),
    path('<int:pk>/update', views.UserUpdateView.as_view()),
    path('<int:pk>', views.UserDetailView.as_view()),
    path('<int:pk>/change-password', views.PasswordUpdateView.as_view()),
]