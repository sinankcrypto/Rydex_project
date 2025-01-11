from django import forms
from .models import product,Variant


class productform(forms.ModelForm):
  class Meta:
    model=product
    fields=['name','description','price','image_main','category','image_1','image_2','image_3']

class Variantform(forms.ModelForm):
  class Meta:
    model=Variant
    fields=['size','stock']