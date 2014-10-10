"""
    Copyright (c) 2014, Jaime Pajuelo.
    All rights reserved.

    Code released under the BSD 2-Clause license.
"""

from django.contrib import admin
from registration.models import ActivationCode


class ActivationCodeAdmin(admin.ModelAdmin):

    actions = None
    list_display = ('get_username', 'get_full_name', 'get_expiration_date', 'is_expired')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = "Full name"

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"

admin.site.register(ActivationCode, ActivationCodeAdmin)
