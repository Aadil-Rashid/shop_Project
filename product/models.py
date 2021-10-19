from django.db import models
from django.utils import timezone
from django.urls import reverse

# I am creating product manager here for ProductModel, which will get only those product who's is_active status is True
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(isActive=True)


class CategoryModel(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=300)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        

    def get_absolute_url(self):
        return reverse('product:category-detail', args=[self.slug])

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    
    category = models.ForeignKey(CategoryModel, related_name="product", on_delete=models.SET_NULL, blank=True, null=True)
    
    title = models.CharField(max_length=70)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    slug = models.SlugField(max_length=255, unique=True)
    # is_active = is product active so that it needs to be displayed on the site
    isActive = models.BooleanField(default=True,) 
    inStock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # I am creating here model manager
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = "Products"
        ordering = ("-created",)   # -created: is stack, thats lastOrder will be shown first in the database

    def get_absolute_url(self):
        return reverse('product:product-detail', args=[self.slug])

    def __str__(self):
        return self.title
