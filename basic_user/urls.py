from django.urls import path
from .import views 


urlpatterns = [
    path('', views.display, name='show'),
    path('<str:house_name>', views.details, name='details'),
]
