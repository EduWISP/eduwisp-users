# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Michele Salerno e i contributori di EduWISP
from django.conf import settings


def environment(request):
    """Avviso di ambiente (per esempio «Ambiente di prova: non inserire dati reali»), ADR-0015."""
    return {"eduwisp_environment_notice": getattr(settings, "EDUWISP_ENVIRONMENT_NOTICE", "")}
