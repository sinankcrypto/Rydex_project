from django import forms
from django.core.validators import MinValueValidator, RegexValidator
from django.core.files.uploadedfile import UploadedFile
from decimal import Decimal
from PIL import Image as PILImage
from .models import product, Variant

class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        min_length=2,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s\-_&]+$',
                message='Product name can only contain letters, numbers, spaces, hyphens, ampersands and underscores.'
            )
        ],
        error_messages={
            'required': 'Product name is required.',
            'min_length': 'Product name must be at least 2 characters long.',
            'max_length': 'Product name cannot exceed 100 characters.'
        }
    )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'), message='Price must be greater than 0.')
        ],
        error_messages={
            'required': 'Price is required.',
            'invalid': 'Please enter a valid price.',
            'max_digits': 'Price cannot exceed 10 digits.',
            'max_decimal_places': 'Price cannot have more than 2 decimal places.'
        }
    )
    
    description = forms.CharField(
        widget=forms.Textarea,
        min_length=10,
        max_length=1000,
        error_messages={
            'required': 'Description is required.',
            'min_length': 'Description must be at least 10 characters long.',
            'max_length': 'Description cannot exceed 1000 characters.'
        }
    )

    class Meta:
        model = product
        fields = ['name', 'description', 'price', 'image_main', 'category', 'image_1', 'image_2', 'image_3', 'is_active']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if not name:
                raise forms.ValidationError('Product name cannot be only whitespace.')
            
            # Check if a product with this name exists (case-insensitive)
            existing_product = product.objects.filter(name__iexact=name)
            if self.instance and self.instance.pk:
                existing_product = existing_product.exclude(pk=self.instance.pk)
                
            if existing_product.exists():
                raise forms.ValidationError('A product with this name already exists (case-insensitive).')
                
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if description:
            description = description.strip()
            if len(description) < 10:
                raise forms.ValidationError('Description must be at least 10 characters long.')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Price must be greater than 0.')
        return price

    def _validate_image(self, image, field_label="Image"):
        if not image or not isinstance(image, UploadedFile):
            return image
        
        # Validate file size (max 5MB)
        if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(f'{field_label} file size cannot exceed 5MB.')
        
        # Validate file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        file_name = getattr(image, 'name', '').lower()
        if not any(file_name.endswith(x) for x in valid_extensions):
            raise forms.ValidationError(f'{field_label} format unsupported. Please use JPG, JPEG, PNG, or WebP.')

        # Verify actual image integrity with Pillow
        try:
            img_copy = PILImage.open(image)
            img_copy.verify()
            if hasattr(image, 'seek'):
                image.seek(0)
        except Exception:
            raise forms.ValidationError(f'{field_label} is invalid or corrupted.')

        return image

    def clean_image_main(self):
        image = self.cleaned_data.get('image_main')
        return self._validate_image(image, "Main product image")

    def clean_image_1(self):
        image = self.cleaned_data.get('image_1')
        return self._validate_image(image, "Additional image 1")

    def clean_image_2(self):
        image = self.cleaned_data.get('image_2')
        return self._validate_image(image, "Additional image 2")

    def clean_image_3(self):
        image = self.cleaned_data.get('image_3')
        return self._validate_image(image, "Additional image 3")

    def clean(self):
        cleaned_data = super().clean()
        image_main = cleaned_data.get('image_main')
        
        # If new product or editing without an existing image
        if not image_main:
            if not self.instance or not self.instance.pk or not self.instance.image_main:
                self.add_error('image_main', 'Main product image is required.')
        
        return cleaned_data


class VariantForm(forms.ModelForm):
    size = forms.ChoiceField(
        choices=Variant.SIZE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select size'
        }),
        error_messages={
            'required': 'Please select a size.',
            'invalid_choice': 'Please select a valid size.'
        }
    )
    
    stock = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter stock quantity'
        }),
        error_messages={
            'required': 'Stock quantity is required.',
            'min_value': 'Stock cannot be negative.',
            'invalid': 'Please enter a valid integer number.'
        }
    )

    def __init__(self, *args, product_instance=None, **kwargs):
        self.product_instance = product_instance
        super().__init__(*args, **kwargs)

    class Meta:
        model = Variant
        fields = ['size', 'stock']

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('Stock cannot be negative.')
        return stock

    def clean(self):
        cleaned_data = super().clean()
        size = cleaned_data.get('size')

        if self.product_instance and size:
            # Check if a variant with this size already exists for the product
            existing_variant = Variant.objects.filter(
                product=self.product_instance,
                size=size,
                is_deleted=False
            )
            
            # If editing, exclude the current instance
            if self.instance and self.instance.pk:
                existing_variant = existing_variant.exclude(pk=self.instance.pk)
            
            if existing_variant.exists():
                raise forms.ValidationError(f"A variant with size '{size}' already exists for this product.")
        
        return cleaned_data