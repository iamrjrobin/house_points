from django.urls import path
from .import views 


urlpatterns = [
    path('', views.display, name='show'),
    path('logs/',views.taking_logs, name = 'logger'),
    path('<str:house_name>/', views.details, name='details'),
]
