from django.shortcuts import render, get_object_or_404
from .models import CategoryModel, ProductModel


def homePageView(request):
    products = ProductModel.products.all()
    context ={'products':products, }
    return render(request, 'home.html', context)
    

def productDetailView(request, slug):
    product = get_object_or_404(ProductModel, slug=slug, inStock=True)
    context = {'product':product}
    return render(request, 'product/detailPage.html', context)


def categoryDetailView(request, categorySlug):
    category = get_object_or_404(CategoryModel, slug=categorySlug)
    products = ProductModel.products.filter(category=category)

    context ={'products':products, 'category':category}

    return render(request, 'product/categoryDetail.html', context)
