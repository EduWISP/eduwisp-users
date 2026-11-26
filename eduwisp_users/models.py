# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Michele Salerno e i contributori di EduWISP
import uuid

from django.conf import settings
from django.db import models


class Organization(models.Model):
    """Tenant: un istituto o una rete di istituti. I dati di tenant diversi sono separati."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("nome", max_length=200)
    slug = models.SlugField("identificativo", unique=True)
    is_active = models.BooleanField("attiva", default=True)
    created_at = models.DateTimeField("creata il", auto_now_add=True)

    class Meta:
        verbose_name = "organizzazione"
        verbose_name_plural = "organizzazioni"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Role(models.TextChoices):
    """Ruoli del prototipo. L'elenco completo è nella documentazione (gestione scolastica)."""

    SCHOOL_ADMIN = "school_admin", "amministratore dell'istituto"
    IT_ADMIN = "it_admin", "amministratore IT"
    TEACHER = "teacher", "docente"


class Membership(models.Model):
    """Appartenenza di un utente a un'organizzazione, con un ruolo."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField("ruolo", max_length=32, choices=Role.choices)
    created_at = models.DateTimeField("creata il", auto_now_add=True)

    class Meta:
        verbose_name = "appartenenza"
        verbose_name_plural = "appartenenze"
        constraints = [
            models.UniqueConstraint(fields=["user", "organization"], name="membership_unica")
        ]

    def __str__(self):
        return f"{self.user} — {self.organization} ({self.get_role_display()})"


class OrganizationOwned(models.Model):
    """Base astratta per i modelli che appartengono a un'organizzazione (tenant)."""

    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name="organizzazione"
    )

    class Meta:
        abstract = True

    #: Campi ForeignKey che devono appartenere alla stessa organizzazione.
    same_organization_fields: tuple[str, ...] = ()

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()
        errors = {}
        for name in self.same_organization_fields:
            related = getattr(self, name, None)
            if related is not None and related.organization_id != self.organization_id:
                errors[name] = "Deve appartenere alla stessa organizzazione."
        if errors:
            raise ValidationError(errors)
