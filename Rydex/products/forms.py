from django import forms
from django.core.validators import MinValueValidator, RegexValidator
from django.db.models import Q
from decimal import Decimal
from .models import product,Variant

class ProductForm(forms.ModelForm):
    # Custom field definitions with validators
    name = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s\-_]+$',
                message='Name can only contain letters, numbers, spaces, hyphens and underscores'
            )
        ],
        error_messages={
            'required': 'Product name is required',
            'max_length': 'Name cannot exceed 100 characters'
        }
    )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'), message='Price must be greater than 0')
        ],
        error_messages={
            'required': 'Price is required',
            'invalid': 'Please enter a valid price',
            'max_digits': 'Price cannot exceed 10 digits',
            'max_decimal_places': 'Price cannot have more than 2 decimal places'
        }
    )
    
    description = forms.CharField(
        widget=forms.Textarea,
        min_length=10,
        max_length=1000,
        error_messages={
            'required': 'Description is required',
            'min_length': 'Description must be at least 10 characters',
            'max_length': 'Description cannot exceed 1000 characters'
        }
    )

    class Meta:
        model = product
        fields = ['name', 'description', 'price', 'image_main', 'category', 'image_1', 'image_2', 'image_3']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Get the current instance if we're editing
        instance = getattr(self, 'instance', None)
        
        # Check if a product with this name exists (case insensitive)
        existing_product = product.objects.filter(name__iexact=name)
        
        # If we're editing, exclude the current instance from the check
        if instance and instance.pk:
            existing_product = existing_product.exclude(pk=instance.pk)
            
        if existing_product.exists():
            raise forms.ValidationError('A product with this name already exists')
            
        return name

    def clean_image_main(self):
        image = self.cleaned_data.get('image_main')
        if image:
            # Validate file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size cannot exceed 5MB')
            
            # Validate file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            ext = str(image.name).lower()[-5:]
            if not any(ext.endswith(x) for x in valid_extensions):
                raise forms.ValidationError('Unsupported file extension. Please use JPG, JPEG, PNG or WebP')
        
        return image

    def clean(self):
        cleaned_data = super().clean()
        # Validate that at least one image is provided
        if not cleaned_data.get('image_main'):
            raise forms.ValidationError('Main product image is required')
        
        return cleaned_data

class VariantForm(forms.ModelForm):
  size = forms.ChoiceField(
    choices=Variant.SIZE_CHOICES,
    widget=forms.Select(attrs={
      'class': 'form-select',
      'placeholder': 'Select size'
    }),
    error_messages={
      'required': 'Please select a size',
      'invalid_choice': 'Please select a valid size'
    }
  )
  
  stock = forms.IntegerField(
    min_value=0,
    widget=forms.NumberInput(attrs={
      'class': 'form-control',
      'placeholder': 'Enter stock quantity'
    }),
    error_messages={
      'required': 'Stock quantity is required',
      'min_value': 'Stock cannot be negative',
      'invalid': 'Please enter a valid number'
    }
  )

  def __init__(self, *args, product_instance=None, **kwargs):
    self.product_instance = product_instance
    super().__init__(*args, **kwargs)

  class Meta:
    model = Variant
    fields = ['size', 'stock']

  def clean(self):
    cleaned_data = super().clean()
    size = cleaned_data.get('size')

    if self.product_instance and size:
      # Check if a variant with this size already exists for the product
      existing_variant = Variant.objects.filter(
        product=self.product_instance,
        size=size
      )
      
      # If we're editing, exclude the current instance
      if self.instance and self.instance.pk:
        existing_variant = existing_variant.exclude(pk=self.instance.pk)
      
      if existing_variant.exists():
        raise forms.ValidationError(f"A variant with size {size} already exists for this product")
    
    return cleaned_data