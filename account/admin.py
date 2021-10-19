from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


from .models import Customer, Address

admin.site.register(Address)

# admin.site.register(UserBase)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'is_active', 'first_name', 'last_name', 'mobile_number', ]
    list_filter = ['is_active', 'is_staff', 'is_superuser',]
    ordering = ('created',)

# class CustomUserAdmin(UserAdmin):
#     """Define admin model for custom User model with no username field."""
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                        'groups', 'user_permissions')}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('email', 'first_name', 'last_name', 'is_staff')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)


# admin.site.register(get_user_model(), CustomUserAdmin)












# from django.conf import settings
#or
# admin.site.register(settings.AUTH_USER_MODEL)

