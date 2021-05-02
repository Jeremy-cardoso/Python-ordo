#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.
Tests pour le module ordonnancement.
"""
import pytest
from ordonnancement import Activite, EDT, Probleme, Tache


@pytest.fixture
def taches():
    """Crée 4 taches."""
    probleme = Probleme.par_str(
        """
A / 1 / 
B / 2 / A
C / 3 / A B
D / 4 / A
"""
    )
    return list(probleme.taches)


@pytest.fixture
def activites():
    """4 activites bateaux."""
    probleme = Probleme.par_str(
        """
A / 1 / 
B / 2 / A
C / 3 / A B
D / 4 / A
"""
    )
    a, b, c, d = probleme.taches
    return [
        Activite(tache=a, debut=0, fin=1, dta=0),
        Activite(tache=b, debut=1, fin=3, dta=1),
        Activite(tache=c, debut=3, fin=6, dta=3),
        Activite(tache=d, debut=1, fin=5, dta=2),
    ]


def test_verification_activite():
    """Compatbilité."""
    a = Tache(nom="A", duree=2, prerequis=[])
    with pytest.raises(ValueError):
        Activite(tache=a, debut=0, fin=1)


def test_instanciation(activites):
    """Création."""
    edt = EDT(activites=activites)
    assert isinstance(edt, EDT)


def test_repr():
    """Pour débogguer."""
    edt = EDT(
        activites=[
            Activite(
                tache=Tache(nom="A", duree=1, prerequis=[]), debut=0, fin=1
            )
        ]
    )
    assert (
        repr(edt)
        == """EDT(activites=[Activite(tache=Tache(nom='A', duree=1, prerequis=[]), debut=0, fin=1)])""".strip()
    )


def test_egalite(activites):
    """Et pas l'identité."""
    assert EDT(activites) == EDT(activites)


def test_activites(activites):
    """Test de la propriété."""
    edt = EDT(activites)
    assert "activites" not in vars(edt)
    assert activites == list(edt.activites)


def test_acces(activites):
    """Test de []."""
    edt = EDT(activites)
    assert edt["A"] == activites[0]


def test_ajoute():
    """Mutation de l'EDT."""
    edt = EDT(activites=[])
    assert edt._activites == []
    tache = Activite(
        tache=Tache(nom="A", duree=1, prerequis=[]), debut=0, fin=1
    )
    edt.ajoute(tache)
    assert edt._activites == [tache]


def test_verification_duree_activites():
    """Au moment de l'ajout."""
    edt = EDT(activites=[])
    with pytest.raises(ValueError):
        edt.ajoute(
            Activite(
                tache=Tache(nom="A", duree=2, prerequis=[]), debut=0, fin=1
            )
        )


def test_verification_doublon(activites):
    """Au moment de l'ajout."""
    edt = EDT(activites=activites)
    with pytest.raises(ValueError):
        edt.ajoute(
            Activite(
                tache=Tache(nom="A", duree=2, prerequis=[]), debut=0, fin=2
            )
        )


def test_valide(activites):
    """Cas ok."""
    edt = EDT(activites)
    assert edt.est_valide()


def test_invalide(activites):
    """Cas pas ok."""
    a, b, c, d = activites
    d.debut = 0
    edt = EDT(activites=[a, b, c, d])
    assert not edt.est_valide()
    
def test_date_valide(activites):
    "test si on a bien le chemin critique"""
    a, b, c, d = activites
    edt = EDT(activites=[a,b,c])
    assert date_valide(activites) == edt
    
    
def activites_2():
    """4 activites bateaux."""
    probleme = Probleme.par_str(
        """
A / 1 / 
B / 2 / A
C / 3 / A B
D / 4 / A
"""
    )
    a, b, c, d = probleme.taches
    return [
        Activite(tache=a, debut=0, fin=1, dta=0),
        Activite(tache=b, debut=1, fin=3, dta=1),
        Activite(tache=c, debut=3, fin=6, dta=3),
        Activite(tache=d, debut=1, fin=5, dta=3560),
    ]    

def test_date_valide(activites_2):
    """Pour vérifier si il repère l'incohérence"""
    resultat=date_valide(activites_2)
    assert resultat == False
    
def test_datevalide(activites):
    """ savoir si il fait bien son travail"""
    resultat = date_valide(activites)
    assert resultat == True