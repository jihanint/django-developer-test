from django import forms
from .models import Product
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'barcode', 'price', 'stock']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        barcode = cleaned_data.get("barcode")

        # Check for duplicate name
        if name:
            qs_name = Product.objects.filter(name=name)
            if self.instance.pk:
                qs_name = qs_name.exclude(pk=self.instance.pk)
            if qs_name.exists():
                raise ValidationError("A product with this name already exists.")

        # Check for duplicate barcode
        if barcode:
            qs_barcode = Product.objects.filter(barcode=barcode)
            if self.instance.pk:
                qs_barcode = qs_barcode.exclude(pk=self.instance.pk)
            if qs_barcode.exists():
                raise ValidationError("A product with this barcode already exists.")

        return cleaned_data
