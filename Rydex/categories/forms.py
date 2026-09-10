from django import forms
from django.core.validators import RegexValidator
from django.core.files.uploadedfile import UploadedFile
from PIL import Image as PILImage
from .models import categories

class categoryform(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        min_length=2,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s\-&_]+$',
                message='Category name can only contain letters, numbers, spaces, hyphens, ampersands and underscores.'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter category name',
        }),
        error_messages={
            'required': 'Category name is required.',
            'min_length': 'Category name must be at least 2 characters long.',
            'max_length': 'Category name cannot exceed 100 characters.',
        }
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter category description',
            'rows': 4,
        }),
        error_messages={
            'max_length': 'Description cannot exceed 500 characters.',
        }
    )

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        }),
        error_messages={
            'invalid_image': 'Upload a valid image file. The file you uploaded was either not an image or a corrupted image.'
        }
    )

    class Meta:
        model = categories
        fields = ['name', 'description', 'is_listed', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if not name:
                raise forms.ValidationError('Category name cannot be only whitespace.')
            
            # Case-insensitive duplicate check
            qs = categories.objects.filter(name__iexact=name)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError('A category with this name already exists (case-insensitive).')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if description:
            description = description.strip()
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and isinstance(image, UploadedFile):
            # Check file size (max 5MB)
            if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size cannot exceed 5MB.')

            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            file_name = getattr(image, 'name', '').lower()
            if not any(file_name.endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError('Unsupported file format. Please upload JPG, JPEG, PNG, or WebP.')

            # Verify actual image integrity
            try:
                img_copy = PILImage.open(image)
                img_copy.verify()
                if hasattr(image, 'seek'):
                    image.seek(0)
            except Exception:
                raise forms.ValidationError('Invalid image file or corrupted image.')

        return image
