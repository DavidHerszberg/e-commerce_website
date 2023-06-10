from django import forms
from django.contrib import admin
from django.forms.utils import ErrorList
from django.http import JsonResponse
from .validators import validate_is_csv
from .models import Attribute, AttributeOption, Product


class ProductImportForm(forms.Form):
    csv_file = forms.FileField(widget=forms.FileInput(attrs={'accept':'text/csv'}), label='קובץ CSV' , validators=[validate_is_csv])

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        # Add validation for file type, size, etc. if needed
        return csv_file

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = []
    
    def __init__(self, product, *args, **kwargs):
        attributes = Attribute.objects.all()
        super().__init__(*args, **kwargs)
        
        for attr in attributes:
            field_name = attr.name
            if attr.multiple_choice:
                self.fields[field_name] = forms.ModelMultipleChoiceField(queryset=attr.אפשרויות.all(), widget=admin.widgets.FilteredSelectMultiple(field_name, False, ), label=field_name, required=False)
                self.fields[field_name].initial = product.סינונים.filter(attribute=attr)
            else:
                self.fields[field_name] = forms.ModelChoiceField(queryset=attr.אפשרויות.all(), label=field_name, required=False)
                try:
                    self.fields[field_name].initial = product.סינונים.get(attribute=attr)
                except: pass