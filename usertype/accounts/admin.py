from django.contrib import admin
from accounts.models import  Pet, User
from typing import Set
from django.contrib.auth.admin import UserAdmin

# class CustomUserAdmin(UserAdmin):
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     is_superuser = request.user.is_superuser
    #     disabled_fields = set()

    #     if not is_superuser:
    #         disabled_fields |= {
    #             'username',
    #             'is_superuser',
    #             'user_permissions',
    #         }

    #     # Prevent non-superusers from editing their own permissions
    #     if (
    #         not is_superuser
    #         and obj is not None
    #         and obj == request.user
    #     ):
    #         disabled_fields |= {
    #             'is_staff',
    #             'is_superuser',
    #             'groups',
    #             'user_permissions',
    #         }

    #     for f in disabled_fields:
    #         if f in form.base_fields:
    #             form.base_fields[f].disabled = True

    #     return form

    # actions = [
    #     'activate_users',
    # ]

    # def activate_users(self, request, queryset):
    #     assert request.user.has_perm('auth.change_user')
    #     cnt = queryset.filter(is_active=False).update(is_active=True)
    #     self.message_user(request, 'Activated {} users.'.format(cnt))
    # activate_users.short_description = 'Activate Users'

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if not request.user.has_perm('auth.change_user'):
    #         del actions['activate_users']
    #     return actions

admin.site.register(Pet)
# admin.site.register(User,CustomUserAdmin)
