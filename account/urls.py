from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from .import views
from .forms import (PwdResetConfirmForm, PwdResetForm, UserLoginForm)

app_name = 'account'


urlpatterns = [

    path('register/', views.registerView, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.accountActivateView, name="activate"),

    # User DashBoard
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('profile/edit/', views.userEditView, name='edit-user-details'),
    path('profile/delete_user/', views.userDeleteView, name='delete-user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="account/delete_confirm.html"), name='delete-confirmation'),

    # login classed based views
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html', form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html',), name='logout'),


    # Reset Password Process
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="account/password_reset/reset_form.html",
        success_url='password_reset_email_confirm',
        email_template_name='account/password_reset/reset_email.html',
        form_class=PwdResetForm), 
        name='pwdreset'),

    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset/reset_confirm.html',
        success_url='/account/password_reset_complete/',
        form_class=PwdResetConfirmForm),
        name="password_reset_confirm"),

    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/password_reset/reset_status.html"), name='password_reset_done'),

    path('password_reset_complete/',
         TemplateView.as_view(template_name="account/password_reset/reset_status.html"), name='password_reset_complete'),

    # Addresses
    path("addresses/", views.addressView, name="addresses"),
    path("add_address/", views.addAddressView, name="add_address"),
    path("addresses/edit/<slug:id>/", views.editAddressView, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.deleteAddressView, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.defaultAddressView, name="set_default"),

]
