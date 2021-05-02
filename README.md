# Python ordonnancement
Projet Python
# Python-ordonnancement
Problème d'ordonnancement
# Objectif

Notre objectif est de résoudre n'importe quel problème d'ordonnancement, peut importe sa durée ou nombre de tâches nous devons toujours trouver une solution ou signaler quand il n'y en a pas.

# Composition d'un problème :

- Chaque problème est composé d'une tâche nommée "A" ,"B" etc... Pour que cette tâche puisse se faire il faut regarder ses prérequis, dans le cas ou elle n'en a pas on peut la faire dès le début.
- En revanche, bien souvient il s'avère que pour qu'une tâche soit lançée il faut que ses prérequis soit finis.
- Chaque tâche admet donc une durée qui est le temps d'execution de la tâche, pour qu'une tâche soit lancée il faut que la durée de l'ensemble de ses prérequis soit finis.

# Composition des modules

# Problème

Ce module sert à la construction de notre problème d'ordonnancement. Il régit toutes les erreurs associées aux mauvaises constructions de nos objets. Il régit également toutes les constructions de nos classes. Il permet aussi de représenter correctement notre problème d'ordonnancement sous forme de tableau.

La classe problème définit :

- La Durée
- Une Tâche
- Un Prérequis

Une tâche dans la construction est composée de :
- Un nom de tâche (A, B, C etc...)
- Un prérequis (tâche'A' ayant pour prérequis 'C')
- Une durée d'execution

On peut ajouter une tâche soit par constructeur alternatif ou soit manuellement via Probleme.

Des fonction pour savoir si le problème respecte les durées positives ou qu'il n'y a pas d'incohérence sont disponibles.

A noter que les tâches et noms de taches sont itérables

# EDT


L'emplois du temps, lui, construit la classe activité qui rajoute et affiche une activité qui englobe une tâche et qui contient :
- Un Début $\rightarrow$ qui est donc la date au plus tôt à laquelle une date peut commencer.
- Une fin $\rightarrow$ qui est donc le début + la durée d'une tâche, la fin d'un prérequis est donc le début d'une autre tâche.
- Une dta $\rightarrow$ qui est la date au plus tard maximum qu'une tâche peut être effectuée sans pour autant compromettre l'intégrité du projet.
- Une marge $\rightarrow$ qui est donc la marge en terme de semaine qu'une tâche peut avoir.

cette classe sert aussi à afficher l'ensemble des résultats fournis pour l'algorithme sous forme de tableau, des fonctions permettants de voir le chemin critique et les maximums de marges ont aussi été rajoutées.



# algorithme 

Sa principale utilité réside dans le fait qu'il résout le problème d'ordonnancement et renvoie ça sous forme d'EDT afin de permettre son affichage, il contient également toutes les fonctions permettant de calculer une date au plus tard, ou une marge, de ranger un problème de maniere croissante ou décroissante etc...

Sa résolution se fait par NetworkX grace surtout au nx.topological_sort qui résout le graphe du problème.

# Autocritique

J'ai pu réaliser les résultats que j'ai voulus démontrer et documenter en testant mes fonctions sur le concept de date au plus tard et marges, néanmoins les fonctions sont "presque" automatisées mais pas complétement car je dois coller le résultat dans une fonction au lieu de faire appel à celle-ci.

Un autre point négatif est que je n'ai pas pu faire la résolution dans le cadre de livraison séquentielle du fait que les marges m'ont déjà prit du temps lors de la conception de celles-ci, j'aurais aimé les faire en y appliquant les marges pour vraiment comparer les différences avec les livraisons en simultannées.
