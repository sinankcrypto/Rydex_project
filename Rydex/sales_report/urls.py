from django.urls import path
from .views import sales_report

urlpatterns = [
    
    path('admin_dashboard/', sales_report, name='admin_dashboard'),
]