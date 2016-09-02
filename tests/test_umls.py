#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uts import umls


def test_retrieve_concept():
    concept = umls.retrieve_concept('C0009044')

    assert concept['ui'] == 'C0009044'
