Title: BOINC, systemd et priorité des processus sous Linux, la suite
Date: 2017-10-25 07:39
Author: Paul
Tags: BOINC, Linux, Libre, systemd
Slug: boinc-systemd-et-priorite-des-processus-sous-linux-la-suite
Lang: fr

Dans mon [précédent billet]({filename}boinc-systemd-et-priorite-des-processus-sous-linux.md) j'avais pensé
avoir réglé mon problème, le démon BOINC laissant toutes les ressources
processeur libres en cas de besoin.  

Pour cela j'avais configuré systemd pour allouer une priorité faible au
cgroup contenant les processus de calculs BOINC:  
`sudo systemctl set-property boinc.service CPUWeight=1`  

Comme noté dans les commentaires, cet attribut n'est pas disponible dans
les versions de systemd antérieures à 231, où il remplace l'attribut
CPUShares.  

L'équivalent pour ces versions est:
`systemctl set-property boinc.service CPUShares=2`  

Ce changement reflète une modification de l'interface cgroups du noyau,
où l'attribut cpu.shares est remplacé par cpu.weight. Or cette
modification n'a pas encore été intégrée dans la branche principale, ce
qui conduit systemd à [convertir la valeur de CPUWeight à son équivalent
cpu.shares](https://github.com/systemd/systemd/blob/4c701096002fff540d9ddb3b21398c551ac3af78/src/core/cgroup.c#L732)
sur mon système.

Pourtant j'ai remarqué que la lecture de vidéos n'était pas fluide sur
mon système. En renouvelant l'expérience précédemment décrite les
résultats montraient que BOINC ne laissait pas libres toutes les
ressources du processeur.  

Après avoir lu quelque documentation comme la [page de manuel de systemd
sur la gestion des
ressources](https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html)
et la [documentation du noyau sur les
cgroups](https://www.kernel.org/doc/Documentation/cgroup-v2.txt), j'ai
pu comprendre d'où venait le problème.  

Les cgroups sont organisés hiérarchiquement. Les ressources processeur
définies dans un cgroup sont partagées entre les cgroups ayant le même
parent.  

De plus systemd utilise une hiérarchie spécifique pour grouper les
processus du système, nommée slices. systemd sépare les processus
utilisés par des services et ceux utilisés par les sessions utilisateurs
dans des slices différentes, user.slice et system.slice, qui font partie
de la slice racine .slice. Ceci peut-être observé avec la commande
`systemd-cgls`qui représente un arbre des processus, services et slices.
Ces slices sont ensuite reflétées dans l'organisation des cgroups créés
par systemd.  

Le service BOINC est donc lancé dans la slice system.slice, comme la
plupart des autres services. Cela signifie qu'il partage son temps
processeur avec les autres service dans cette slice selon la
configuration CPUWeight donnée, et que la slice partage cette ressource
avec les autres slices selon leurs configurations propres.  

La configuration pour la slice contenant les services et celle contenant les
sessions des utilisateurs est celle-ci:

```
% cat /sys/fs/cgroup/cpu/system.slice/cpu.shares

1024  

% cat /sys/fs/cgroup/cpu/user.slice/cpu.shares

1024  
```

Les deux slices ont donc le même nombre de shares configuré. Le résultat
est que si chacune demande toutes les ressources processeur disponible,
chacune aura 50% du temps disponible alloué. Et donc dans le cas de
BOINC, l'utilisateur n'a que 50% du temps processeur disponible !  

Une solution est de créer une slice dédiée pour BOINC, et de lui allouer
une faible priorité.  

On procède en créant la configuration de la slice dans le fichier
`/etc/systemd/system/lowprio.slice` qui a le contenu suivant:  

```
[Unit]  

Description=Slice with low CPU priority  

DefaultDependencies=no  

Before=slices.target  

[Slice]  

CPUWeight=1  
```

Ensuite on surcharge la configuration du service BOINC en créant un
fichier `/etc/systemd/system/boinc.service` avec le contenu suivant:  

```
.include /usr/lib/systemd/system/boinc.service  

[Service]  

Slice=lowprio.slice  
```

Finalement on recharge la configuration de systemd et redémarre le
service BOINC:  

```
% sudo systemctl daemon-reload  

% sudo systemctl restart boinc.service  
```

On peut maintenant relance la même expérience qu'auparavant, mais en
utilisant la commande `systemd-cgtop` qui montre l'utilisation du
processeur par groupe:  
```
Control Group Procs %CPU Memory Input/s Output/s  

/ 72 558.4 5.1G - -  

/lowprio.slice 8 520.0 - - -  

/user.slice 47 33.8 - - -  

/system.slice 16 2.9 - - -  

/init.scope 1 - - - -  

/lowprio.slice/boinc.service 8 - - - -  
```

On remarque que boinc.service n'a pas de temps CPU comptabilisé. C'est
parce que j'ai retiré l'attribut CPUWeight pour le service, ce qui
désactive le suivi de l'utilisation processeur de son cgroup. Ce n'est
pas un problème car le cgroup parent lowprio.slice le comptabilise, et
utilise environ 558% de temps processeur.  

On relance l'expérimentation en lançant la commande
`` % for i in `seq 8`; do sha512sum /dev/zero&;done ``.  

Cette fois cgtop montre que toutes les ressources processeurs sont
attribuées à la slice contenant les sessions utilisateurs user.slice:  
```
Control Group Procs %CPU Memory Input/s Output/s  

/ 80 800.0 5.4G - -  

/user.slice 55 784.4 - - -  

/lowprio.slice 8 10.8 - - -  

/system.slice 16 4.0 - - -  

/init.scope 1 - - - -  

/lowprio.slice/boinc.service 8 - - - -  
```  

On note que system.slice est aussi utilisée car le serveur d'affichage
Xorg est lancé dans cette slice, et je joue une vidéo en parallèle. Il
faut donc allouer une priorité suffisante à ce groupe pour ne pas
impacter la vitesse d'affichage.  

Pour conclure on peut noter que l'utilisation des cgroups et de systemd
a fortement compliqué la configuration de l'allocation des ressources
processeur du système. Il m'a fallu pas mal de temps pour comprendre
comment revenir au comportement voulu par BOINC, c'est à dire de laisser
toutes les ressources processeur disponibles quand n'importe quel autre
programme en a besoin.

