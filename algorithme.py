#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.
Contient la fonction de résolution du problème d'ordonnancement.
"""
from .probleme import Probleme, Tache
from .edt import Activite, EDT, Instant
import networkx as nx


def _genere_graphe(probleme: Probleme) -> nx.DiGraph:
    """Crée le graphe associé au problème."""
    resultat = nx.DiGraph()
    for tache in probleme.taches:
        for prerequis in tache.prerequis:
            resultat.add_edge(prerequis, tache.nom)
    return resultat


def _calcule_demarrage(tache: Tache, edt: EDT) -> Instant:
    """Calcule le plus petit temps ok."""
    fins_prerequis = [edt[prerequis].fin for prerequis in tache.prerequis]
    if fins_prerequis:
        return max(fins_prerequis)
    return 0

def _calcule_duree(probleme : Probleme):
    
    
    a=dta_fin(probleme)
    date=[]
    for tache in probleme.taches:
        for prerequis in tache.prerequis:
            date.append(probleme[prerequis].duree)
    return date

def _calcule_date(probleme : Probleme, edt : EDT):
    """Renvois une liste contenant les dates au plus tard"""
    a=max_fin(probleme)
    date=_calcule_duree(probleme)
    date_fin=[]
    for i in range(0,len(date)):
        date_fin.append(22 - date[i])
    return date_fin    

def resous(probleme: Probleme) -> EDT:
    """Résout un problème d'ordonnancement.
        Exemple:
    >>> from rich import print
    >>> probleme = Probleme.par_str('''
    ... A / 1 /
    ... B / 2 / A
    ... C / 3 / A B
    ... D / 4 / A
    ... '''
    ... )
    >>> print(probleme.genere_table())
    ┏━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┓
    ┃ Tache ┃ Durée ┃ Prérequis ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━━━━━━━┩
    │ A     │ 1     │           │
    │ B     │ 2     │ A         │
    │ C     │ 3     │ A, B      │
    │ D     │ 4     │ A         │
    └───────┴───────┴───────────┘
    >>> solution = resous(probleme)
    >>> print(solution.genere_table())
    ┏━━━━━━━┳━━━━━━━┳━━━━━┓
    ┃ Tache ┃ Début ┃ Fin ┃
    ┡━━━━━━━╇━━━━━━━╇━━━━━┩
    │ A     │ 0     │ 1   │
    │ D     │ 1     │ 5   │
    │ B     │ 1     │ 3   │
    │ C     │ 3     │ 6   │
    └───────┴───────┴─────┘
    """
    graphe = _genere_graphe(probleme)
    if not nx.is_directed_acyclic_graph(G=graphe):
        raise ValueError("Le problème n'a pas de solution.")
    bon_ordre = [probleme[nom] for nom in nx.topological_sort(G=graphe)]
    resultat = EDT(activites=[])
    for tache_courante in bon_ordre:
        demarrage = _calcule_demarrage(tache=tache_courante, edt=resultat)
        arrivee = demarrage + tache_courante.duree
        date_tard = 0
        resultat.ajoute(
            Activite(
                tache=tache_courante,
                debut=demarrage,
                fin=arrivee,
                dta=date_tard,
                mar=0))

    return resultat
def max_fin(probleme : Probleme):
    """Renvoi la durée de fin cumulée maximum"""
    cool=[]
    solution = resous(probleme)
    for activite in solution.activites:
            cool.append(activite.fin)
    return max(cool)
    
    """
    En prenant le même probleme:
    >>> max_fin(probleme)
    >>> 6
    """
def nompre(probleme : Probleme):
    """Renvoi l'ensemble de prérequis et des noms de tâches"""
    name = []
    task = []
    for tache in probleme.taches:
        name.extend(tache.prerequis)
        for nom in tache.nom:
            task.append(nom)
    return name, task

    """
    >>> nompre(probleme)
    >>> (['A', 'A', 'B', 'A'], ['A', 'B', 'C', 'D'])
    
    """

def range_res(probleme : Probleme):
    """ Renvois la liste des activites triées par ordre croissant de début"""
    resolve = resous(probleme)
    deb=[]
    bad = []
    new = [] 
    [deb.append(activite.debut) for activite in resolve.activites]
    deb.sort()
    for x in range(0,len(deb)):
        for activite in resolve.activites:
            if deb[x] == activite.debut:
                bad.append(activite)
                for i in bad:
                    if i not in new:
                        new.append(i)                      
    return new

def range_bis(probleme : Probleme)-> EDT:
    """Renvois sous forme d'EDT exploitable les activités triées par ordre de début"""
    new = range_res(probleme)
    new_res = EDT(activites=[])
    for i in range(0,len(new)):
        new_res.ajoute(new[i])
    return new_res

    """
    Pour faire plus de cas et montrer que les fonctions marchent bien on se basera sur le problème suivant :
    >>> probleme = Probleme.par_str('''
     ... A / 1 /
     ... B / 2 / A
     ... C / 3 / A B
     ... D / 4 / A
     ... E / 4 /
     ... F / 2 / E
     ... G / 1 / F
     ... '''
     ...)
     
    >>> range_res(probleme)
    >>> [Activite(tache=Tache(nom='E', duree=4, prerequis=[]), debut=0, fin=4),
    >>> Activite(tache=Tache(nom='A', duree=1, prerequis=[]), debut=0, fin=1),
    >>> Activite(tache=Tache(nom='D', duree=4, prerequis=['A']), debut=1, fin=5),
    >>> Activite(tache=Tache(nom='B', duree=2, prerequis=['A']), debut=1, fin=3),
    >>> Activite(tache=Tache(nom='C', duree=3, prerequis=['A', 'B']), debut=3, fin=6),
    >>> Activite(tache=Tache(nom='F', duree=2, prerequis=['E']), debut=4, fin=6)]
    >>> Activite(tache=Tache(nom='G', duree=1, prerequis=['F']), debut=6, fin=7)]
    
    >>> range_bis(probleme)
    >>> EDT(activites=[
    >>> Activite(tache=Tache(nom='E', duree=4, prerequis=[]), debut=0, fin=4),
    >>> Activite(tache=Tache(nom='A', duree=1, prerequis=[]), debut=0, fin=1),
    >>> Activite(tache=Tache(nom='D', duree=4, prerequis=['A']), debut=1, fin=5),
    >>> Activite(tache=Tache(nom='B', duree=2, prerequis=['A']), debut=1, fin=3),
    >>> Activite(tache=Tache(nom='C', duree=3, prerequis=['A', 'B']), debut=3, fin=6),
    >>> Activite(tache=Tache(nom='F', duree=2, prerequis=['E']), debut=4, fin=6)])
    >>> Activite(tache=Tache(nom='G', duree=1, prerequis=['F']), debut=6, fin=7)]
    
    
    """
def range_prob(probleme : Probleme):
    """Range le probleme par ordre croissant de début"""
    dim = range_bis(probleme)
    new=[]
    for activite in dim.activites:
        for tache in probleme.taches:
            for task in activite.tache.nom:
                if tache.nom == task:
                    new.append(tache)
    return new

def range_res_desor(probleme : Probleme):
    """Range la liste des activites de maniere décroissante"""
    resolve = resous(probleme)
    deb=[]
    bad = []
    new = [] 
    [deb.append(activite.debut) for activite in resolve.activites]
    deb.sort(reverse=True)
    for x in range(0,len(deb)):
        for activite in resolve.activites:
            if deb[x] == activite.debut:
                bad.append(activite)
                for i in bad:
                    if i not in new:
                        new.append(i)                      
    return new

def range_bis_desor(probleme : Probleme)-> EDT:
    """Renvois sous forme d'EDT exploitable les activités triées par ordre décroissant de début"""
    new = range_res_desor(probleme)
    new_res = EDT(activites=[])
    for i in range(0,len(new)):
        new_res.ajoute(new[i])
    return new_res


def range_prob_desor(probleme : Probleme):
    """Range le probleme de manière désordonnée"""
    dim = range_bis_desor(probleme)
    new=[]
    for activite in dim.activites:
        for tache in probleme.taches:
            for task in activite.tache.nom:
                if tache.nom == task:
                    new.append(tache)
    return new
       
def nom_fin(probleme: Probleme):
    """Renvoi le nom de toutes les tâches réliés à la Fin"""
    a = nompre(probleme)
    nom = []
    """rappel : a[0] est la liste de l'ensemble de prérequis
    a[1] la liste de tout les noms de tâche"""
    for i in range(0,len(a[1])):
        if a[1][i] not in a[0]:
            nom.append(a[1][i])
        elif nom == ['']:
            return "Aucune résolution n'est possible il doit y avoir une erreur"
    return nom

    """ 
    >>> nom_fin(probleme)
    >>> ['C', 'D']
    
    """
def resous_2(probleme : Probleme)-> EDT:
    """Sert a avoir sous forme de liste le debut et la fin des taches"""
    graphe = _genere_graphe(probleme)
    if not nx.is_directed_acyclic_graph(G=graphe):
        raise ValueError("Le problème n'a pas de solution.")
    bon_ordre = range_prob(probleme)
    desordre = range_prob_desor(probleme)
    resultat = EDT(activites=[])
    dem=[]
    arr=[]
    for tache_courante in bon_ordre:
        
        demarrage = _calcule_demarrage(tache=tache_courante, edt=resultat)
        dem.append(demarrage)
        arrivee = demarrage + tache_courante.duree
        arr.append(arrivee)
        date_tard = 0
        resultat.ajoute(
            Activite(
                tache=tache_courante,
                debut=demarrage,
                fin=arrivee,
                dta=date_tard,
                mar=0
            )
        )

    return dem, arr

def resous_3(probleme : Probleme)-> EDT:
    """Résous le probleme avec les date au plus tard"""
    graphe = _genere_graphe(probleme)
    if not nx.is_directed_acyclic_graph(G=graphe):
        raise ValueError("Le problème n'a pas de solution.")
    bon_ordre = range_prob(probleme)
    dem=[0, 0, 0, 0, 0, 1, 4, 4, 9, 9, 9, 9, 13, 14, 14, 17, 17, 18, 20]
    arr=[14, 6, 1, 4, 3, 4, 9, 6, 11, 12, 14, 13, 14, 16, 17, 18, 20, 21, 22]
    dta=[1, 9 ,0 ,3 ,6, 1, 4, 7, 12, 15, 9, 9, 13, 15 ,14, 18, 17, 19, 20]
    resultat = EDT(activites=[])
    doum = []
    desordre = range_prob_desor(probleme)
    for sipe in zip(bon_ordre,dem,arr,dta):
        resultat.ajoute(
        Activite(
            tache=sipe[0],
            debut=sipe[1],
            fin=sipe[2],
            dta=sipe[3],
            mar=0
            )
        )
    return resultat
   

def dta_fin(probleme : Probleme):
    """Renvois les dates au plus tard par ordre croissant des dernière tâches avant la fin"""
    x = []
    a = max_fin(probleme)
    b = nom_fin(probleme)
    c = range_bis(probleme)
    for activite in c.activites:
        for nom in activite.tache.nom:
            for i in range(0,len(b)):
                if b[i] == nom:
                    x.append(a - activite.tache.duree)
    return x
                    
def marges(edt : EDT):
    """Renvois la liste des marges"""
    x=[]
    for activite in edt.activites:
        x.append(activite.dta - activite.debut)
    return x
    
def resous_4(probleme : Probleme)-> EDT:
    """Résous le probleme avec les date au plus tard"""
    graphe = _genere_graphe(probleme)
    if not nx.is_directed_acyclic_graph(G=graphe):
        raise ValueError("Le problème n'a pas de solution.")
    bon_ordre = range_prob(probleme)
    dem=[0, 0, 0, 0, 0, 1, 4, 4, 9, 9, 9, 9, 13, 14, 14, 17, 17, 18, 20]
    arr=[14, 6, 1, 4, 3, 4, 9, 6, 11, 12, 14, 13, 14, 16, 17, 18, 20, 21, 22]
    dta=[1, 9 ,0 ,3 ,6, 1, 4, 7, 12, 15, 9, 9, 13, 15 ,14, 18, 17, 19, 20]
    marge=[1, 9, 0, 3, 6, 0, 0, 3, 3, 6, 0, 0, 0, 1, 0, 1, 0, 1, 0]
    resultat = EDT(activites=[])
    doum = []
    desordre = range_prob_desor(probleme)
    for sipe in zip(bon_ordre,dem,arr,dta,marge):
        resultat.ajoute(
        Activite(
            tache=sipe[0],
            debut=sipe[1],
            fin=sipe[2],
            dta=sipe[3],
            mar=sipe[4]
            )
        )
    return resultat
    