from django.urls import path
from .views import sales_report

urlpatterns = [   
    path('admin/sales_report/', sales_report, name='sales_report'),
]