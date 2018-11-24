Title: DVBT2MPGF: Pas de disque DVB-T trouvé
Date: 2009-09-21 13:47
Author: Dominique
Tags: Logiciels
Slug: dvbt2mpgf-pas-de-disque-dvb-t-trouve
Lang: fr

J'ai reçu de nombreux mails concernant des problèmes de reconnaissance
des disques des PVR SAGEM sous DVBT2MPG. Le disque dur de mon PC a
soudainement arrêté de fonctionner et j'ai perdu tous mes mails
(heureusement j'avais des sauvegardes de tout le reste). Je ne peux donc
plus répondre à chacun. Veuillez m'en excuser.  

Avec les fichiers .log qui m'ont été transmis j'ai pu analyser le
problème: il semble que SAGEM ait changé le processeur de ses terminaux
et que le nouveau ne range pas les nombres de la même façon en mémoire.
En effet ce processeur place l'octet de poids le plus faible à l'adresse
la plus faible (« Little Endian » comme pour les processeurs x86
d’Intel) alors que le processeur précédant rangeait l’octet de poids le
plus fort à l’adresse la plus faible (« Big Endian » comme les
processeurs ex-Motorola).  

J’ai mis en ligne une nouvelle version de DVBT2MPG (V1R2.3) qui détecte
automatiquement le sexe des nombres ! Je n’ai malheureusement aucun
moyen de la tester. Donc si quelqu’un qui a rencontré le problème
pouvait faire un essai avec cette nouvelle version et me faire part du
résultat…  

Remarque concernant le fonctionnement sous Vista : par défaut Vista
n’autorise pas l’accès direct aux secteurs du disque. Il faut donc
changer les propriétés du fichier DVBT2MPG.EXE (ou DVBT2MPGF.EXE) afin
qu’il s’exécute en tant qu’ « Administrateur » (ça s’applique aussi à
Windows 7).


