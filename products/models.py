from django.db import models
import os

def get_product_image_path(instance, filename):
    # Get the file extension
    ext = os.path.splitext(filename)[1]
    # Construct the image filename using the store ID and file extension
    image_filename = f"{instance.store_id}{ext}"
    # Return the path to store the image
    return os.path.join('product_images/', image_filename)

def get_manufacturer_logo_path(instance, filename):
    # Get the file extension
    ext = os.path.splitext(filename)[1]
    # Construct the logo filename using the manufacturer's name and replace spaces with underscores
    logo_filename = f"{instance.name.replace(' ', '_')}{ext}"
    # Return the path to store the logo
    return os.path.join('manufacturer_logos/', logo_filename)

def get_supplier_logo_path(instance, filename):
    # Get the file extension
    ext = os.path.splitext(filename)[1]
    # Construct the logo filename using the supplier's name and replace spaces with underscores
    logo_filename = f"{instance.name.replace(' ', '_')}{ext}"
    # Return the path to store the logo
    return os.path.join('supplier_logos/', logo_filename)


class Product(models.Model):
    store_id = models.CharField(max_length=100, unique=True, verbose_name='מקט')
    gtin = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='GTIN')
    hebrew_name = models.CharField(max_length=255, unique=True, verbose_name="שם")
    english_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="שם באנגלית")
    description = models.TextField(blank=True, null=True, verbose_name="תיאור")
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="יצרן")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="מחיר")
    inventory = models.PositiveIntegerField(default=0, verbose_name="מלאי")
    product_link = models.URLField(blank=True, null=True, verbose_name="קישור לאתר יצרן")
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ספק")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="מחיר עלות")
    main_image = models.ForeignKey(
        'Image',
        related_name='main_products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="תמונה ראשית",
        )

    def __str__(self):
        return self.hebrew_name

    class Meta:
        verbose_name = 'מוצר'
        verbose_name_plural = 'מוצרים'

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="שם")
    logo = models.ImageField(upload_to=get_manufacturer_logo_path, blank=True, null=True, verbose_name="לוגו")
    website = models.URLField(blank=True, null=True, verbose_name="קישור")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'יצרן'
        verbose_name_plural = 'יצרנים'

class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="שם")
    logo = models.ImageField(upload_to=get_supplier_logo_path, blank=True, null=True, verbose_name="לוגו")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ספק'
        verbose_name_plural = 'ספקים'

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images', verbose_name="קובץ")

    def __str__(self) -> str:
        return self.image.url.split('/')[-1]
    
    class Meta:
        verbose_name = "תמונה"
        verbose_name_plural = "תמונות"

class Attribute(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="שם")
    multiple_choice = models.BooleanField(default=True, verbose_name='אפשר ריבוי בחירות')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'סינון'
        verbose_name_plural = 'סינונים'

class AttributeOption(models.Model):
    attribute = models.ForeignKey('Attribute', related_name='אפשרויות', on_delete=models.CASCADE)
    text = models.CharField(max_length=100, verbose_name='טקסט')
    image = models.ImageField(upload_to='attribute_images', blank=True, null=True, verbose_name='קובץ')
    products = models.ManyToManyField('Product', related_name='סינונים', blank=True, verbose_name='מוצרים')

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = 'אפשרות סינון'
        verbose_name_plural = 'אפשרויות סינון'