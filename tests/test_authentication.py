#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uts.authentication import Authenticator
from uts.settings import SERVICES
import pytest

service_data = list(SERVICES.keys())


def test_authentication():
    ticket_granting_ticket = Authenticator().ticket_granting_ticket

    assert 'http' in ticket_granting_ticket


@pytest.mark.parametrize("service", service_data)
def test_get_service_ticket(service):
    service_ticket = Authenticator().get_service_ticket(service)

    assert 'ST-' in service_ticket
