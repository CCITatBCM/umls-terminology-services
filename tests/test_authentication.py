#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uts.authentication import Authentication
from uts.settings import SERVICES
import pytest

service_data = list(SERVICES.keys())


def test_authentication():
    ticket_granting_ticket = Authentication().ticket_granting_ticket

    assert 'http' in ticket_granting_ticket


@pytest.mark.parametrize("service", service_data)
def test_get_service_ticket(service):
    service_ticket = Authentication().get_service_ticket(service)

    assert 'ST-' in service_ticket
