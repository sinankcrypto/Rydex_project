from django import forms
from .models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            'code',
            'discount',
            'max_discount',
            'min_order_amount',
            'active',
            'valid_from',
            'valid_to',
        ]
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_order_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'code': 'Coupon Code',
            'discount': 'Discount (%)',
            'max_discount': 'Maximum Discount',
            'min_order_amount': 'Minimum Order Amount',
            'active': 'Active',
            'valid_from': 'Valid From',
            'valid_to': 'Valid To',
        }
        help_texts = {
            'discount': 'Enter the discount as a percentage (e.g., 10 for 10%).',
            'max_discount': 'Maximum discount amount (e.g., 100).',
            'min_order_amount': 'Minimum order value to apply this coupon.',
        }
