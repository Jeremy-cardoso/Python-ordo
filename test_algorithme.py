#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.
Teste la fonction de résolution.
"""
import pytest
from ordonnancement import Activite, EDT, Probleme, resous


def test_sans_solution():
    """Doit planter."""
    probleme = Probleme.par_str(
        """
A / 1 / B
B / 2 / A
"""
    )
    with pytest.raises(ValueError):
        resous(probleme)


def test_solution():
    """Attention à l'ordre sinon il faut modifier l'égalité entre deux EDT!"""
    probleme = Probleme.par_str(
        """
A / 1 / 
B / 2 / A
C / 3 / A B
D / 4 / A
"""
    )
    solution = resous(probleme)
    a, b, c, d = probleme.taches
    edt = EDT(
        activites=[
            Activite(a, debut=0, fin=1),
            Activite(d, debut=1, fin=5),
            Activite(b, debut=1, fin=3),
            Activite(c, debut=3, fin=6),
        ]
    )
    assert solution == edt
    
    
def test_max_fin():
    """test si la valeur affichée est toujours la maximum"""
    result = max_fin(probleme)
    assert result == 6
    
def test_nompre():
    "test si les noms et les prérequis renvoyés sont bons"""
    result = nompr(probleme)
    assert result == (['A', 'A', 'B', 'A'], ['A', 'B', 'C', 'D'])
    
def test_nom_fin():
    """test si les noms affiché sont les bons"""
    result = nom_fin(probleme)
    assert result == ['C', 'D']
    
def test_range_bis():
    """test si la liste est la bonne"""
    probleme = Probleme.par_str(
        """
A / 1 / 
B / 2 / A
C / 3 / A B
D / 4 / A
E / 4 /
F / 2 / E
G / 1 / F
"""
    )
    solution = resous(probleme)
    a, b, c, d, e, f, g = probleme.taches
    edt = EDT(
        activites=[
            Activite(e, debut=0, fin=4),
            Activite(a, debut=0, fin=1),
            Activite(d, debut=1, fin=5),
            Activite(b, debut=1, fin=3),
            Activite(c, debut=3, fin=6),
            Activite(f, debut=4, fin=6),
            Activite(g, debut=6, fin=7),
        ]
    )
    assert solution == edt