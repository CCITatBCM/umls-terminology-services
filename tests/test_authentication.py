#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from uts.authentication import Authentication
from uts.settings import API_KEY


def test_get_ticket_granting_ticket():
    ticket_granting_ticket = Authentication().get_ticket_granting_ticket(API_KEY)

    assert 'http' in ticket_granting_ticket


def test_get_service_ticket():
    ticket_granting_ticket = Authentication().get_ticket_granting_ticket(API_KEY)
    service_ticket = Authentication().get_service_ticket(ticket_granting_ticket, 'mti')

    assert 'ST-' in service_ticket
