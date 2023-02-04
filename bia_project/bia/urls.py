from django.urls import path
from bia import views

urlpatterns = [
    path('bia', views.bia_list),
    path('bia/', views.bia_list),
]