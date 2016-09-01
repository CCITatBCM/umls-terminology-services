#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uts.authentication import Authentication


def test_authentication():
    ticket_granting_ticket = Authentication().ticket_granting_ticket

    assert 'http' in ticket_granting_ticket


def test_get_service_ticket():
    service_ticket = Authentication().get_service_ticket('mti')

    assert 'ST-' in service_ticket
