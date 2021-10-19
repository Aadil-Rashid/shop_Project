from django.urls import path
from .import views

app_name = 'product'

urlpatterns = [
    path('', views.homePageView, name='home-page'),
    path('<slug:slug>', views.productDetailView, name="product-detail"),
    path('shop/<slug:categorySlug>/', views.categoryDetailView, name='category-detail'),

]
