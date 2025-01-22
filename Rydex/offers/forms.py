from django import forms
from .models import CategoryOffer,ProductOffer

class CategoryOfferForm(forms.ModelForm):
  class Meta:
    model=CategoryOffer
    fields=['category','discount_percentage','valid_from','valid_to','is_active']

    widgets = {
            'valid_from': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'placeholder': 'DD/MM/YYYY HH:MM',
                'class': 'form-control'
            }),
            'valid_to': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'placeholder': 'DD/MM/YYYY HH:MM',
                'class': 'form-control'
            }),
        }



class ProductOfferForm(forms.ModelForm):
  class Meta:
    model=ProductOffer
    fields=['product','discount_percentage','valid_from','valid_to','is_active']

    widgets = {
            'valid_from': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'placeholder': 'DD/MM/YYYY HH:MM',
                'class': 'form-control'
            }),
            'valid_to': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'placeholder': 'DD/MM/YYYY HH:MM',
                'class': 'form-control'
            }),
        }
