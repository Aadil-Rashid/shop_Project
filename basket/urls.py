from django.urls import path
from .import views

app_name = 'basket'

urlpatterns = [
    path('', views.basketSummaryView, name='basket-summary'),
    path('add/', views.basketAddView, name='basket-add'),
    path('delete/', views.basketdeleteView, name='basket-delete'),
    path('update/', views.basketUpdateView, name='basket-update'),

]
