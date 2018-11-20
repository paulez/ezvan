Title: BOINC, systemd et priorité des processus sous Linux
Date: 2017-10-14 06:35
Author: paul
Slug: boinc-systemd-et-priorite-des-processus-sous-linux

<div
class="field field-name-body field-type-text-with-summary field-label-hidden">

<div class="field-items">

<div class="field-item even">

Je me suis récemment remis à faire tourner
[BOINC](https://boinc.berkeley.edu/) sur ma machine. BOINC est un
logiciel de calcul scentifique distributé. En utilisant BOINC je prête
en quelque sorte la capacité de calcul de mon ordinateur à des projets
de recherche scientifique.

</p>
Le principe de BOINC est de n'utiliser que les ressources libres de la
machine. Il fait de la sorte en attribution une priorité minimale aux
processus qui réalisent le calcul. Sous Linux c'est fait en attribuant
la valeur [nice](https://fr.wikipedia.org/wiki/Nice_(Unix)) maximale aux
processus lancés par BOINC, qui est 19. Plus la valeur nice est élevée,
moins le processus est prioritaire.

</p>
Cette valeur 19 correspond à une priorité idle, ce qui signifie qu'elle
ne permet d'utiliser que le temps restant qui n'est réclamé par aucun
processus plus prioritaire. Cela correspond en pratique à n'utiliser que
les ressources laissées libres sur le machine.

</p>
Cette configuration a fonctionné pendant longtemps sous Linux. Or j'ai
remarqué que sur mon système BOINC ne semblait pas laisser toutes les
ressources libres, car certains de mes programmes étaient plus long à
s’exécuter, et donc mon ordinateur avait l'air plus lent. J'ai donc
voulu vérifier cela. Un moyen simple est d'essayer d'utiliser au maximum
le processeur, et de voir si toutes les ressources étaient disponibles.  

Pour ce faire je lance huit fois (car ma machine a huit processeurs
logiques) une commande qui va utiliser toute la ressource processeur
disponible.

</p>
`` for i in `seq 8`; do sha512sum /dev/zero&;done ``

</p>
En observant l'utilisation du processeur avec la commande top, je
remarque que chacun des processus sha512sum n'obtient que 50% de temps
processeur. De plus le champs ni de top indique une utilisation de 50%
pour les processus à priorité minimale. Normalement elle devrait être de
0 !  

Pourquoi n'est-ce pas le cas ?

</p>
En fait la gestion des priorités de processus sous Linux a été pas mal
compliquée par l'apparition des
[cgroups](https://fr.wikipedia.org/wiki/Cgroups=), ou control groups.
Ces groupes permettent de grouper des ressources du noyau et d'appliquer
des contrôles à ces groupes. Il est ainsi possible de limiter les
ressources utilisées par un groupe de processus.

</p>
Cela introduit une nouvelle hiérarchie pour la priorité des processus.
Dans mon cas tous les processus BOINC sont dans un même cgroup, et les
processus que je lance dans un autre cgroup.

</p>
Les processus BOINC arrivaient toujours à utiliser environ 50% du
système car les ressources processeur sont réparties équitablement entre
ces deux groupes. Tout cela indépendamment des priorités des processus.  

Ce type de mécanique a été implémenté car il était auparavant facile
d'accaparer les ressources d'un système en lançant plein de processus.
En équilibrant les priorités des groupes on évite ce problème.

</p>
Mais dans mon cas je veux que le groupe contenant les processus BOINC
ait une priorité minimale. Ces groupes sont configurés par le système
d'initialisation [systemd](https://fr.wikipedia.org/wiki/Systemd=) qui
gère entre de multiples choses les services systèmes et démarrer les
sessions utilisateurs, et qui les place dans des groupes séparés. Il
suffit donc d'indiquer à systemd de donner une priorité minimale au
group utilisé par BOINC:

</p>
`sudo systemctl set-property boinc.service CPUWeight=1`

</p>
Après avoir lancé cette commande, je relance mon expérience, et cette
fois mes processus de test utilisent bien chacun 100% du processeur.
BOINC ne ralentit donc plus mon ordinateur !

</p>
<p>

</div>

</div>

</div>

<div
class="field field-name-taxonomy-vocabulary-3 field-type-taxonomy-term-reference field-label-above">

<div class="field-label">

Thème: 

</div>

<div class="field-items">

<div class="field-item even">

[Libre](https://www.ezvan.fr/taxonomy/term/48)

</div>

<div class="field-item odd">

[Linux](https://www.ezvan.fr/taxonomy/term/45)

</div>

<div class="field-item even">

[systemd](https://www.ezvan.fr/taxonomy/term/62)

</div>

<div class="field-item odd">

[BOINC](https://www.ezvan.fr/taxonomy/term/63)

</div>

</div>

</div>

</p>

