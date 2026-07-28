from django import forms
from .models import Address
from django.core.validators import RegexValidator

class AddressForm(forms.ModelForm):

    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Enter a valid 10-digit phone number.'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit phone number',
                'maxlength': '10',
                'inputmode': 'numeric',
            }
        )
    )

    pin_code = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Enter a valid 6-digit PIN code.'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter 6-digit PIN code',
                'maxlength': '6',
                'inputmode': 'numeric',
            }
        )
    )

    full_name = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+(?:[A-Za-z ]*[A-Za-z]+)?$',
                message='Name can contain only letters and spaces.'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Full name',
            }
        )
    )

    city = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+(?:[A-Za-z ]*[A-Za-z]+)?$',
                message='City can contain only letters and spaces.'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'City',
            }
        )
    )

    state = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+(?:[A-Za-z ]*[A-Za-z]+)?$',
                message='State can contain only letters and spaces.'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'State',
            }
        )
    )

    class Meta:
        model = Address
        fields = [
            'full_name',
            'phone_number',
            'address_line',
            'city',
            'state',
            'pin_code',
        ]

        widgets = {
            'address_line': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Address',
                }
            ),
        }

class ReturnRequestForm(forms.Form):
  reason = forms.CharField(
    widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter reason for return'}),
    max_length=500,
    required=True
  )