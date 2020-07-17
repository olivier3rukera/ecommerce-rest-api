from django.urls import path
from .api import views

urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('add/', views.ProductCreateView.as_view()),
    path('<uuid:pk>/', views.ProductRetrieveView.as_view()),
    path('categories/', views.CategoryListView.as_view())
]
