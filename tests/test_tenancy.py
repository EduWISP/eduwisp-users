# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Michele Salerno e i contributori di EduWISP
import pytest
from django.contrib.auth import get_user_model

from eduwisp_users.models import Membership, Organization, Role
from eduwisp_users.tenancy import organizations_for

pytestmark = pytest.mark.django_db


@pytest.fixture
def scuole():
    a = Organization.objects.create(name="Istituto Fittizio A", slug="istituto-a")
    b = Organization.objects.create(name="Istituto Fittizio B", slug="istituto-b")
    return a, b


def test_utente_vede_solo_la_propria_organizzazione(scuole):
    a, b = scuole
    utente = get_user_model().objects.create_user("docente.a", password="x")
    Membership.objects.create(user=utente, organization=a, role=Role.TEACHER)
    assert list(organizations_for(utente)) == [a]


def test_filtro_per_ruolo(scuole):
    a, b = scuole
    utente = get_user_model().objects.create_user("tecnico", password="x")
    Membership.objects.create(user=utente, organization=a, role=Role.IT_ADMIN)
    Membership.objects.create(user=utente, organization=b, role=Role.TEACHER)
    assert list(organizations_for(utente, roles=[Role.IT_ADMIN])) == [a]


def test_organizzazione_disattivata_esclusa(scuole):
    a, _ = scuole
    a.is_active = False
    a.save()
    utente = get_user_model().objects.create_user("docente", password="x")
    Membership.objects.create(user=utente, organization=a, role=Role.TEACHER)
    assert not organizations_for(utente).exists()


def test_superuser_vede_tutto(scuole):
    admin = get_user_model().objects.create_superuser("admin", password="x")
    assert organizations_for(admin).count() == 2


def test_attribuzione_nell_interfaccia(client):
    get_user_model().objects.create_superuser("admin", password="x")
    client.login(username="admin", password="x")
    risposta = client.get("/admin/")
    assert "Basato su EduWISP" in risposta.content.decode()


def test_avviso_ambiente_di_prova(client, settings):
    settings.EDUWISP_ENVIRONMENT_NOTICE = "Ambiente di prova: non inserire dati reali"
    get_user_model().objects.create_superuser("admin", password="x")
    client.login(username="admin", password="x")
    assert "Ambiente di prova: non inserire dati reali" in client.get("/admin/").content.decode()


def test_nessun_avviso_se_non_configurato(client):
    get_user_model().objects.create_superuser("admin", password="x")
    client.login(username="admin", password="x")
    assert "eduwisp-notice" not in client.get("/admin/").content.decode()


def test_ruolo_famiglia(scuole):
    a, _ = scuole
    genitore = get_user_model().objects.create_user("genitore")
    Membership.objects.create(user=genitore, organization=a, role=Role.GUARDIAN)
    assert list(organizations_for(genitore, roles=[Role.GUARDIAN])) == [a]
    assert list(organizations_for(genitore, roles=[Role.TEACHER])) == []
