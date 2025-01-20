from django.contrib import admin
from .models import Category, Brand, Product, ProductImage
from django_summernote.admin import SummernoteModelAdmin  # Keep this only if needed for Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('cat_name',)} # for automatic slug adding
    list_display = ('cat_name', 'slug')


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand_name',)}
    list_display = ('brand_name', 'slug')


# Inline for adding images in the product form
class ProductImageInline(admin.TabularInline): 
    model = ProductImage
    extra = 1  # Number of blank image fields to display


class ProductAdmin(SummernoteModelAdmin):  # Use SummernoteModelAdmin only if needed for Product
    summernote_fields = ('description',)  # Remove this line if you're not using Summernote for the description field
    inlines = [ProductImageInline]  # Add the inline to the Product admin
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'price', 'stock', 'category', 'brand', 'modified_date', 'is_available')


# Registering models with their corresponding admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)

