# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Michele Salerno e i contributori di EduWISP
"""Funzioni di isolamento tra tenant, riutilizzabili dagli altri moduli EduWISP."""

from collections.abc import Iterable

from .models import Organization


def organizations_for(user, roles: Iterable[str] | None = None):
    """Organizzazioni a cui l'utente appartiene (tutte per i superuser della piattaforma)."""
    if not user.is_authenticated:
        return Organization.objects.none()
    if user.is_superuser:
        return Organization.objects.all()
    qs = Organization.objects.filter(memberships__user=user, is_active=True)
    if roles is not None:
        qs = qs.filter(memberships__role__in=list(roles))
    return qs.distinct()


class OrganizationScopedAdminMixin:
    """Mixin per ModelAdmin: mostra e modifica solo i dati delle proprie organizzazioni.

    Il modello deve avere un campo ``organization`` (vedi ``OrganizationOwned``).
    """

    organization_roles: Iterable[str] | None = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization__in=organizations_for(request.user, self.organization_roles))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            orgs = organizations_for(request.user, self.organization_roles)
            related = db_field.related_model
            if db_field.name == "organization":
                kwargs["queryset"] = orgs
            elif any(f.name == "organization" for f in related._meta.get_fields()):
                # Nei menu compaiono solo oggetti delle proprie organizzazioni.
                kwargs["queryset"] = related._default_manager.filter(organization__in=orgs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def _has_org_access(self, request, obj):
        if obj is None or request.user.is_superuser:
            return True
        return (
            organizations_for(request.user, self.organization_roles)
            .filter(pk=obj.organization_id)
            .exists()
        )

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj) and self._has_org_access(request, obj)

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and self._has_org_access(request, obj)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and self._has_org_access(request, obj)
