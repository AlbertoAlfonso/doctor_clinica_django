from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models

class UserAdmin(BaseUserAdmin):
   ordering = ['id']
   list_display = ['username', 'email', 'name']
   fieldsets = (
       (None, {'fields': ('username', 'email', 'password')}),
       (_('Personal Info'), {'fields': ('name',)}),
       (
           _('Permissions'),
           {'fields': ('is_active', 'is_staff', 'is_superuser')}
       ),
       (_('Important Dates'), {'fields':('last_login',)})
   )
   add_fieldsets = [
       (None, {
           'classes': ('wide',),
           'fields': ('username', 'email', 'password1', 'password2')
       }),
   ]

# admin.site.register(models.User, UserAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Patient)
admin.site.register(models.Doctor)
admin.site.register(models.Petition)