# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Michele Salerno e i contributori di EduWISP
from django.contrib import admin

from .models import Membership, Organization


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    autocomplete_fields = ["user"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "created_at"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}
    inlines = [MembershipInline]

    def has_module_permission(self, request):
        # La gestione delle organizzazioni è riservata agli amministratori della piattaforma.
        return request.user.is_superuser


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "organization", "role", "created_at"]
    list_filter = ["role", "organization"]
    autocomplete_fields = ["user", "organization"]

    def has_module_permission(self, request):
        return request.user.is_superuser
