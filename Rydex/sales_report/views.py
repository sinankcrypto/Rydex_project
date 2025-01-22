from django.shortcuts import render
from order.models import Order

# Create your views here.

def sales_report_view(request):
    # Aggregate sales data
    total_orders = Order.objects.count()
    total_sales = Order.objects.aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
    total_discount = Order.objects.aggregate(total_discount=models.Sum('discount'))['total_discount'] or 0

    # Orders breakdown by date
    daily_sales = (
        Order.objects.filter(status='Delivered')
        .extra({'day': "DATE(created_at)"})
        .values('day')
        .annotate(total=models.Sum('amount'))
        .order_by('-day')
    )

    context = {
        'total_orders': total_orders,
        'total_sales': total_sales,
        'total_discount': total_discount,
        'daily_sales': daily_sales,
    }
    return render(request, 'admin/sales_report.html', context)