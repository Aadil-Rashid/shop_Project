from django.urls import path
from .import views


app_name = 'payment'


urlpatterns = [
    path('', views.paymentPageView, name='payment-page'),
    path('handlerequest/', views.handlerequest, name = 'handlerequest'),
]
