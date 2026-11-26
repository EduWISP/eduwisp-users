# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Michele Salerno e i contributori di EduWISP
from django.apps import AppConfig


class EduwispUsersConfig(AppConfig):
    name = "eduwisp_users"
    verbose_name = "EduWISP — utenti e organizzazioni"
    default_auto_field = "django.db.models.BigAutoField"
