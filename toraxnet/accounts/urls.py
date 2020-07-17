from django.urls import path
from .api import views

urlpatterns = [
    path('sign/admin/', views.AdminToken.as_view()),
    path('sign/in/', views.ObtainAuthToken.as_view()),
    path('sign/up/', views.CreateUser.as_view())
]