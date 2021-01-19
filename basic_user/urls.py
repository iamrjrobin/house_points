from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views as view
from rest_framework.authtoken.views import obtain_auth_token

from . import views

# from core import views as core_views

schema_view = get_schema_view(
   openapi.Info(
      title="House API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/api-token-auth/', view.obtain_auth_token, name = 'token'),
    path('', views.display, name='show'),
    path('signup/', views.signup_view, name = 'signup'),
    path('login/', views.login_view, name='login'),
    path('logs/single_log/<int:employee_id>/',views.single_log, name = 'single_log'),
    path('logs/',views.taking_logs, name = 'logger'),
    path('<int:house_id>/', views.details, name='details'),
    path('api/signup', views.api_signup, name = 'api_signup'),
    path('api/login', obtain_auth_token, name = 'api_login'),
    path('api/display/', views.api_display, name = 'api_show'),
    path('api/display/<int:house_id>', views.api_details, name = 'api_details'),
    path('api/display/find/<int:house_id>', views.Emp_list_view.as_view(), name = 'emp_list_view'),
    path('api/logs', views.api_taking_logs, name = 'api_logger'),
    path('api/logs/single_logs/<int:employee_id>',views.api_single_log, name = 'api_single_log'),
    path('api/show_all_emp/',  views.api_all_emp, name = 'show_all_emp'),
    path('api/api_all_emp_update/<int:employee_id>',views.api_all_emp_update, name = 'api_all_emp_update'), 
    path('api/api_all_emp_partial_update/<int:house_id>/<int:employee_id>',views.api_all_emp_partial_update, name = 'api_all_emp_partial_update'),
    path('api/api_points/', views.api_points, name = 'api_points'),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('oauth/', include('social_django.urls', namespace='social')),
    
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]



