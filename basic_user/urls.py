from django.urls import path, include
from .import views 


urlpatterns = [
    path('', views.display, name='show'),
    path('logs/single_log/<int:employee_id>/',views.single_log, name = 'single_log'),
    path('logs/',views.taking_logs, name = 'logger'),
    path('<int:house_id>/', views.details, name='details'),
    path('api/display/', views.api_display),
    path('api/display/<int:house_id>', views.api_details),
    path('api/display/find/<int:house_id>', views.Emp_list_view.as_view()),
    path('api/logs', views.api_taking_logs),
    path('api/logs/single_logs/<int:employee_id>',views.api_single_log),
    path('api/show_all_emp/',  views.api_all_emp),
    path('api/api_points/', views.api_points),
]



