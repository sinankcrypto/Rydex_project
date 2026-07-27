from django import forms
from .models import categories

class categoryform(forms.ModelForm):
  class Meta:
    model=categories
    fields=['name','description','is_listed','image']

    widgets = {
      'name': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Enter category name',
      }),

      'description': forms.Textarea(attrs={
          'class': 'form-control',
          'placeholder': 'Enter category description',
          'rows': 4,
      }),

      'image': forms.ClearableFileInput(attrs={
          'class': 'form-control',
      }),
  }
