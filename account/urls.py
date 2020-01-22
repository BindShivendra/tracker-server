from django.urls import path

from . import views


urlpatterns = [
    path('', views.UserListView.as_view()),
    path('register', views.UserRegisterView.as_view()),
    path('<slug:slug>/update', views.UserUpdateView.as_view()),
    path('<slug:pslugk>/change-password', views.PasswordUpdateView.as_view()),
    path('<slug:slug>/detail', views.UserDetailView.as_view()),
]