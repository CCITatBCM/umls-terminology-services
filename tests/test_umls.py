#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uts import umls

test_cui = 'C0155502'
concept = umls.Concept(test_cui)


def test_concept_get():
    details = concept.get()

    assert details is not False


def test_concept_atoms():
    atoms = concept.atoms(sabs='MSH', language='ENG')

    assert atoms is not False


def test_concept_atoms_preferred():
    atoms = concept.atoms_preferred(sabs='SNOMEDCT_US', language='ENG')

    assert atoms is not False


def test_concept_definitions():
    definitions = concept.definitions()

    print(definitions)

    assert definitions is not False
