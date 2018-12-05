Title: BOINC, systemd et priorité des processus sous Linux
Date: 2017-10-14 06:35
Author: Paul
Tags: Libre, Linux, systemd, BOINC
Slug: boinc-systemd-et-priorite-des-processus-sous-linux
Lang: fr

Je me suis récemment remis à faire tourner
[BOINC](https://boinc.berkeley.edu/) sur ma machine. BOINC est un
logiciel de calcul scentifique distributé. En utilisant BOINC je prête
en quelque sorte la capacité de calcul de mon ordinateur à des projets
de recherche scientifique.

Le principe de BOINC est de n'utiliser que les ressources libres de la
machine. Il fait de la sorte en attribution une priorité minimale aux
processus qui réalisent le calcul. Sous Linux c'est fait en attribuant
la valeur [nice](https://fr.wikipedia.org/wiki/Nice_(Unix)) maximale aux
processus lancés par BOINC, qui est 19. Plus la valeur nice est élevée,
moins le processus est prioritaire.

Cette valeur 19 correspond à une priorité idle, ce qui signifie qu'elle
ne permet d'utiliser que le temps restant qui n'est réclamé par aucun
processus plus prioritaire. Cela correspond en pratique à n'utiliser que
les ressources laissées libres sur la machine.

Cette configuration a fonctionné pendant longtemps sous Linux. Or j'ai
remarqué que sur mon système BOINC ne semblait pas laisser toutes les
ressources libres, car certains de mes programmes étaient plus long à
s’exécuter, et donc mon ordinateur avait l'air plus lent. J'ai donc
voulu vérifier cela. Un moyen simple est d'essayer d'utiliser au maximum
le processeur, et de voir si toutes les ressources étaient disponibles.  

Pour ce faire je lance huit fois (car ma machine a huit processeurs
logiques) une commande qui va utiliser toute la ressource processeur
disponible.

`` for i in `seq 8`; do sha512sum /dev/zero&;done ``

En observant l'utilisation du processeur avec la commande top, je
remarque que chacun des processus sha512sum n'obtient que 50% de temps
processeur. De plus le champ "ni" de top indique une utilisation de 50%
pour les processus à priorité minimale. Normalement elle devrait être de
0 !  

Pourquoi n'est-ce pas le cas ?

En fait la gestion des priorités de processus sous Linux a été pas mal
compliquée par l'apparition des
[cgroups](https://fr.wikipedia.org/wiki/Cgroups), ou control groups.
Ces groupes permettent de grouper des ressources du noyau et d'appliquer
des contrôles à ces groupes. Il est ainsi possible de limiter les
ressources utilisées par un groupe de processus.

Cela introduit une nouvelle hiérarchie pour la priorité des processus.
Dans mon cas tous les processus BOINC sont dans un même cgroup, et les
processus que je lance dans un autre cgroup.

Les processus BOINC arrivaient toujours à utiliser environ 50% du
système car les ressources processeur sont réparties équitablement entre
ces deux groupes. Tout cela indépendamment des priorités des processus.  

Ce type de mécanique a été implémenté car il était auparavant facile
d'accaparer les ressources d'un système en lançant plein de processus.
En équilibrant les priorités des groupes on évite ce problème.

Mais dans mon cas je veux que le groupe contenant les processus BOINC
ait une priorité minimale. Ces groupes sont configurés par le système
d'initialisation [systemd](https://fr.wikipedia.org/wiki/Systemd) qui
gère entre de multiples choses les services systèmes et démarrer les
sessions utilisateurs, et qui les place dans des groupes séparés. Il
suffit donc d'indiquer à systemd de donner une priorité minimale au
group utilisé par BOINC:

`sudo systemctl set-property boinc.service CPUWeight=1`

Après avoir lancé cette commande, je relance mon expérience, et cette
fois mes processus de test utilisent bien chacun 100% du processeur.
BOINC ne ralentit donc plus mon ordinateur !

