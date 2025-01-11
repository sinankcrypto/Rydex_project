from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    fields = ['full_name', 'phone_number', 'address_line', 'city', 'state', 'pin_code']
    widgets = {
      'full_name': forms.TextInput(attrs={'class': 'form-control'}),
      'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
      'address_line': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
      'city': forms.TextInput(attrs={'class': 'form-control'}),
      'state': forms.TextInput(attrs={'class': 'form-control'}),
      'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
    }