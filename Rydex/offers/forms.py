from django import forms
from .models import CategoryOffer,ProductOffer
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    
    def clean_discount_percentage(self):
        discount = self.cleaned_data['discount_percentage']

       
        if discount < 0 or discount > 80:
            raise ValidationError("Discount percentage must be between 0 and 80.")
       
        return discount

    def clean(self):
       cleaned_data = super().clean()
       valid_from = cleaned_data.get('valid_from')
       valid_to = cleaned_data.get('valid_to')

       if valid_from and valid_from < timezone.now():
           self.add_error('valid_from', "Offer start date cannot be in the past.")

       if valid_from and valid_to:
           if valid_to <= valid_from:
               self.add_error('valid_to', "End date must be later than start date.")

       return cleaned_data
    
    def clean_category(self):
        category = self.cleaned_data['category']
        
        # Check if the product already has an active offer
        existing_offers = CategoryOffer.objects.filter(
            category=category, 
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_to__gte=timezone.now()
        )
        
        # If this is an edit of an existing offer, exclude the current offer from the check
        if self.instance.pk:
            existing_offers = existing_offers.exclude(pk=self.instance.pk)
        
        if existing_offers.exists():
            raise ValidationError("This category already has an active offer.")
        
        return category



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
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate product has no active offers
        product = cleaned_data.get('product')
        if product:
            existing_offers = ProductOffer.objects.filter(
                product=product, 
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            
            if self.instance.pk:
                existing_offers = existing_offers.exclude(pk=self.instance.pk)
            
            if existing_offers.exists():
                raise ValidationError("This product already has an active offer.")

        # Validate dates
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')
        
        if valid_from and valid_to:
            if valid_to <= valid_from:
                raise ValidationError("End date must be later than start date.")
            
            if valid_from < timezone.now():
                raise ValidationError("Offer start date cannot be in the past.")

        # Validate discount percentage
        discount = cleaned_data.get('discount_percentage')
        if discount is not None and (discount < 0 or discount > 80):
            raise ValidationError("Discount percentage must be between 0 and 80.")

        return cleaned_data