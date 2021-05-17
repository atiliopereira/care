from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from sistema.forms import UsuarioForm
from sistema.models import Usuario


class UsuarioInline(admin.StackedInline):
    model = Usuario
    form = UsuarioForm
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
