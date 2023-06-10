import csv, io, requests
from typing import Any, Dict, List, Optional, Tuple
from django.http.request import HttpRequest
from django import forms
from django.core.files import File
from django.core.files.storage import default_storage
from django.db import IntegrityError, models
from django.contrib import admin, messages
from .models import Product, Manufacturer, Supplier, Image, Attribute, AttributeOption
from .forms import ProductImportForm, ProductAttributeForm
from django.urls import path
from django.template.response import TemplateResponse
from legima.shared import admin_site_titles
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE
from django.forms import inlineformset_factory


def add_extra_context(context, extra, page_title=None):
    if extra:
        for k in extra['extra_context']:
            context[k] = extra['extra_context'][k]
            if page_title:
                context['page_title'] = page_title
    return context

class ImageInline(admin.TabularInline):
    model = Image
    fields = ['image', 'תמונה']
    readonly_fields = ['תמונה']
    extra = 0
    ordering = ['-main_products']
    classes = ['collapse']
    def תמונה(self, obj):
        return mark_safe("""<img src="/%s" height=100 />""" % obj.image)

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['main_image'].queryset = self.instance.images.all()

        attributes = Attribute.objects.all()
        for attr in attributes:
            field_name = attr.name
            if attr.multiple_choice:
                self.fields[field_name] = forms.ModelMultipleChoiceField(queryset=attr.אפשרויות.all(), widget=admin.widgets.FilteredSelectMultiple(field_name, False, ), label=field_name, required=False)
                self.fields[field_name].initial = self.instance.סינונים.filter(attribute=attr)
            else:
                self.fields[field_name] = forms.ModelChoiceField(queryset=attr.אפשרויות.all(), label=field_name, required=False)
                try:
                    self.fields[field_name].initial = self.instance.סינונים.get(attribute=attr)
                except: pass


    def save(self, commit=True):
        instance = super().save(commit=False)
        main_image = self.cleaned_data['main_image']
        instance.main_image = main_image if main_image in instance.images.all() else None
        if commit:
            instance.save()
        return instance

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [ImageInline]
    formfield_overrides = {models.TextField: {'widget': TinyMCE()}}
    readonly_fields = ['תצוגה_מקדימה']
    fieldsets = (
            (None, {
                'fields': [
                    ('store_id', 'gtin'),
                    ('hebrew_name', 'english_name'),
                    ('description'),
                    ('main_image', 'תצוגה_מקדימה'),
                    ],
            }
        ),
        
    )
    def תצוגה_מקדימה(self, obj):
        return mark_safe("""<img src="/product_images/%s" height=100 />""" % obj.main_image)


    change_list_template = 'admin/product_change_list.html'
    change_form_template = 'admin/product/change_form.html'

    # def get_fieldsets(self, request: HttpRequest, obj: Any | None = ...) -> List[Tuple[str | None, Dict[str, Any]]]:
    #     fieldsets = super().get_fieldsets(request, obj)
    #     fieldsets[0][1]['fields'].append(self.render_image(obj))
        
    #     return fieldsets
    
    def get_opt_object(self):
        return self.model._meta

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import', self.import_view, name='product_import', kwargs={'extra_context': admin_site_titles}),
            path('<str:product_id>/attributes', self.attribute_view, name='product_attributes', kwargs={'extra_context': admin_site_titles})
        ]
        return custom_urls + urls

    def attribute_view(self, request, product_id ,**kwargs):
        page_title = "סינונים"
        product = Product.objects.get(id=product_id)

        if request.method == 'POST':
            pass

        else:
            form = ProductAttributeForm(product=product)
            context = {
                'form': form,
                'has_change_permission': True,
                'opts': self.get_opt_object(),
            }
            context = add_extra_context(context, kwargs, page_title)
            context |= self.admin_site.each_context(request)
            return TemplateResponse(request, 'admin/product/attribute_form.html', context)

    def import_view(self, request, **kwargs):
        page_title = "ייבוא מוצרים"

        if request.method == 'POST':
            form = ProductImportForm(request.POST, request.FILES)
            if form.is_valid():
                page_title = 'תוצאות ייבוא'
                csv_file = form.cleaned_data['csv_file']
                # Process the uploaded CSV file
                imported_products, failed_lines = self.process_csv_file(csv_file)
                # Display import results to the user
                context = {
                    'imported_products': imported_products,
                    'failed_lines': failed_lines,
                    'total_imported': len(imported_products),
                    'opts': self.get_opt_object(),
                    'has_change_permission': True,
                }
                context = add_extra_context(context, kwargs, page_title)
                context |= self.admin_site.each_context(request)
                return TemplateResponse(request, 'admin/product_import_results.html', context)
        else:
            form = ProductImportForm()
        context = {
            'form': form,
            'opts': self.get_opt_object(),
        }
        context = add_extra_context(context, kwargs, page_title)
        context |= self.admin_site.each_context(request)
        return TemplateResponse(request, 'admin/product_import.html', context)
    
    def process_csv_file(self, csv_file):
        imported_products = []
        failed_lines = []
        csv_data = csv_file.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(csv_data))
        for line_number, row in enumerate(reader, start=1):
            try:
                # Extract product attributes from the CSV row
                store_id = row['store_id']
                gtin = row.get('gtin', None)
                hebrew_name = row['hebrew_name']
                english_name = row.get('english_name', None)
                description = row.get('description', None)
                manufacturer_name = row.get('manufacturer', None)
                price = row['price']
                inventory = row.get('inventory', 0)
                image_path = row.get('image', None)
                supplier_name = row.get('supplier', None)
                cost_price = row.get('cost_price', None)
                product_link = row.get('product_link', None)


                # Link to existing or create manufacturer
                manufacturer, _ = Manufacturer.objects.get_or_create(name=manufacturer_name)

                # Link to existing or create supplier
                supplier, _ = Supplier.objects.get_or_create(name=supplier_name)

                # Handle image upload
                if image_path:
                    # Check if the image path is a URL
                    if image_path.startswith('http://') or image_path.startswith('https://'):
                        # Fetch the image content from the URL
                        response = requests.get(image_path)
                        if response.status_code == 200:
                            # Extract the file name from the URL
                            file_name = f"{store_id}.{image_path.rsplit('.', 1)[-1]}"
                            file_path = f"product_images/{file_name}"
                            # Save the image content to the storage
                            with default_storage.open(file_path, 'wb') as destination:
                                destination.write(response.content)
                        else:
                            raise Exception(f"Failed to download image from URL: {image_path}")
                    else:
                        # Assume the image path is a local file path
                        with default_storage.open(image_path, 'rb') as source:
                            file_name = f"{store_id}.{image_path.rsplit('.', 1)[-1]}"
                            file_path = f"product_images/{file_name}"
                            with default_storage.open(file_path, 'wb') as destination:
                                destination.write(source.read())


                # Create the product
                product = Product.objects.create(
                    store_id=store_id,
                    hebrew_name=hebrew_name,
                    english_name=english_name,
                    description=description,
                    manufacturer=manufacturer,
                    price=price,
                    inventory=inventory,
                    supplier=supplier,
                    cost_price=cost_price,
                    product_link=product_link,
                )
                
                # create the image
                if image_path:
                    image = Image.objects.create(
                        product=product,
                        image=file_path,
                    )
                    product.images.add(image)
                    product.main_image = image

                if gtin and not Product.objects.filter(gtin=gtin).exists():
                    product.gtin = gtin
                    product.save()

                imported_products.append(product)
            except Exception as e:
                failed_lines.append((line_number, str(e)))

        return imported_products, failed_lines

    def changelist_view(self, request, extra_context=admin_site_titles):
        if request.method == 'POST' and '_import' in request.POST:
            return self.import_view(request, extra_context=extra_context)
        return super().changelist_view(request, extra_context)

class AttributeInLine(admin.TabularInline):
    model = AttributeOption
    extra = 0
    fields = ['text', 'image', 'תמונה', 'מוצרים']
    readonly_fields = ['תמונה', 'מוצרים']

    def תמונה(self, obj):
        return mark_safe("""<img src="/%s" height=50 />""" % obj.image)
    
    def מוצרים(self, obj):
        return len(obj.products.all())
    
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeInLine]





admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer)
admin.site.register(Supplier)
admin.site.register(Attribute, AttributeAdmin)