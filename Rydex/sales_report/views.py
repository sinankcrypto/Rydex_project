from django.shortcuts import render
from order.models import Order
from django.db.models import Sum, F
from django.utils.timezone import now, timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import openpyxl
from io import BytesIO

def sales_report(request):
    total_sales_count = Order.objects.count()
    total_sales_amount = Order.objects.aggregate(total=Sum('final_amount'))['total'] or 0
    total_discount = Order.objects.aggregate(discount=Sum(F('amount') - F('final_amount')))['discount'] or 0

    today = now().date()
    daily_sales = Order.objects.filter(created_at__date=today).aggregate(
        total_amount=Sum('final_amount'),
        discount=Sum(F('amount') - F('final_amount')),
    )
    daily_sales_count = Order.objects.filter(created_at__date=today).count()

    week_start = today - timedelta(days=today.weekday())  
    weekly_sales = Order.objects.filter(created_at__date__gte=week_start).aggregate(
        total_amount=Sum('final_amount'),
        discount=Sum(F('amount') - F('final_amount')),
    )
    weekly_sales_count = Order.objects.filter(created_at__date__gte=week_start).count()

    month_start = today.replace(day=1)  
    monthly_sales = Order.objects.filter(created_at__date__gte=month_start).aggregate(
        total_amount=Sum('final_amount'),
        discount=Sum(F('amount') - F('final_amount')),
    )
    monthly_sales_count = Order.objects.filter(created_at__date__gte=month_start).count()

    # Handle filtering
    period = request.GET.get('period', 'daily')
    selected_date = request.GET.get('date', None)

    if not selected_date:
        selected_date = today  
    else:
        selected_date = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()

    # Filter sales based on the selected date and period
    if period == 'daily':
        filtered_sales = Order.objects.filter(created_at__date=selected_date).aggregate(
            total_amount=Sum('final_amount'),
            discount=Sum(F('amount') - F('final_amount')),
        )
        filtered_sales_count = Order.objects.filter(created_at__date=selected_date).count()
    elif period == 'weekly':
        week_start = selected_date - timedelta(days=selected_date.weekday())
        filtered_sales = Order.objects.filter(created_at__date__gte=week_start).aggregate(
            total_amount=Sum('final_amount'),
            discount=Sum(F('amount') - F('final_amount')),
        )
        filtered_sales_count = Order.objects.filter(created_at__date__gte=week_start).count()
    elif period == 'monthly':
        month_start = selected_date.replace(day=1)
        filtered_sales = Order.objects.filter(created_at__date__gte=month_start).aggregate(
            total_amount=Sum('final_amount'),
            discount=Sum(F('amount') - F('final_amount')),
        )
        filtered_sales_count = Order.objects.filter(created_at__date__gte=month_start).count()
    else:
        filtered_sales = {'total_amount': 0, 'discount': 0}
        filtered_sales_count = 0

    context = {
        'filter': period,
        'selected_date': selected_date,
        'total_sales_count': total_sales_count,
        'total_sales_amount': total_sales_amount,
        'total_discount': total_discount,
        'daily_sales': daily_sales,
        'daily_sales_count': daily_sales_count,
        'weekly_sales': weekly_sales,
        'weekly_sales_count': weekly_sales_count,
        'monthly_sales': monthly_sales,
        'monthly_sales_count': monthly_sales_count,
        'filtered_sales': filtered_sales,
        'filtered_sales_count': filtered_sales_count,
    }

    export_format = request.GET.get('export', None)
    if export_format == "pdf":
        return generate_pdf(context)
    elif export_format == "excel":
        return generate_excel(context)

    return render(request, 'admin/sales_report.html', context)


def generate_pdf(context, filename="sales_report.pdf"):
    template = get_template('admin/pdf_template.html')
    html = template.render(context)
    response = BytesIO()
    pdf_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response)
    if pdf_status.err:
        return HttpResponse("Error generating PDF", status=500)
    response = HttpResponse(response.getvalue(), content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def generate_excel(context, filename="sales_report.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sales Report"

    # Add headers
    headers = ["Period", "Sales Count", "Total Amount", "Total Discount"]
    ws.append(headers)

    # Add sales data
    ws.append([
        context['filter'].capitalize(),
        context['filtered_sales_count'],
        context['filtered_sales']['total_amount'],
        context['filtered_sales']['discount']
    ])

    # Write the workbook to a BytesIO object
    response = BytesIO()
    wb.save(response)
    response.seek(0)

    # Return the response as an Excel file
    response = HttpResponse(response, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
