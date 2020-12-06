from django.urls import path
from .import views 


urlpatterns = [
    path('', views.display, name='show'),
    path('logs/single_log/<int:employee_id>/',views.single_log, name = 'single_log'),
    path('logs/',views.taking_logs, name = 'logger'),
    path('<int:house_id>/', views.details, name='details'),
]
