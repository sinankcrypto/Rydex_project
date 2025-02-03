from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
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

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if self.instance.pk:
            # If editing existing coupon, exclude current instance from unique check
            if Coupon.objects.filter(code=code).exclude(pk=self.instance.pk).exists():
                raise ValidationError('This coupon code already exists.')
        else:
            # If creating new coupon
            if Coupon.objects.filter(code=code).exists():
                raise ValidationError('This coupon code already exists.')
        return code

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount is not None and (discount <= 0 or discount > 80):
            raise ValidationError('Discount must be between 0 and 80.')
        return discount

    def clean_max_discount(self):
        max_discount = self.cleaned_data.get('max_discount')
        if max_discount is not None and max_discount <= 0:
            raise ValidationError('Maximum discount must be greater than 0.')
        return max_discount

    def clean_min_order_amount(self):
        min_order_amount = self.cleaned_data.get('min_order_amount')
        if min_order_amount is not None and min_order_amount <= 0:
            raise ValidationError('Minimum order amount must be greater than 0.')
        return min_order_amount

    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')
        now = timezone.now()

        if valid_from:
            if valid_from < now:
                self.add_error('valid_from', 'Valid from date cannot be in the past.')

        if valid_from and valid_to:
            if valid_to < valid_from:
                self.add_error('valid_to', 'Valid to date must be after valid from date.')

        return cleaned_data