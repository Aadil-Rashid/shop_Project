from django.contrib import admin
from .models import ProductModel, CategoryModel

@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created', 'updated']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'slug', 'isActive', 'inStock','created', 'updated']
    list_filter = ['inStock', 'isActive']
    list_editable = ['price', 'isActive', 'inStock']
    prepopulated_fields = {'slug': ('title',)}
