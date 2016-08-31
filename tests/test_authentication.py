#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `medical_text_indexer` module. """

import sys
import pytest

from uts.authentication import Authentication


class TestAuthentication(object):
    @classmethod
    def setup_class(cls):
        cls.authenticator = Authentication('http://skr.nlm.nih.gov/cgi-bin/SKR/Restricted_CAS/API_batchValidationII.pl')
        pass

    def test_get_ticket_granting_ticket(self):
        authenticator = Authentication('http://skr.nlm.nih.gov/cgi-bin/SKR/Restricted_CAS/API_batchValidationII.pl')
        ticket_granting_ticket = authenticator.get_ticket_granting_ticket()

        assert ticket_granting_ticket[:4] == 'http'

    @classmethod
    def teardown_class(cls):
        pass
