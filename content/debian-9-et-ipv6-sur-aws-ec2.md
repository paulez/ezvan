Title: Debian 9 et IPv6 sur AWS EC2
Date: 2018-01-09 00:32
Author: Paul
Tags: Libre, Debian, EC2, IPv6, Linux
Slug: debian-9-et-ipv6-sur-aws-ec2

Ce week-end j'ai configuré [IPv6](https://fr.wikipedia.org/wiki/IPv6)
sur mon infrastructure [EC2](https://aws.amazon.com/ec2/) qui tourne
sous [Debian 9](https://wiki.debian.org/fr/DebianStretch). J'ai suivi
[le guide fourni par
AWS](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpc-migrate-ipv6.html),
mais j'ai rencontré quelques soucis, et ce guide n'a pas d'instructions
pour Debian. Je vous conseille fortement de réaliser ces changements
d'abord sur des instances de tests, car mes premiers essais ont rendus
mes instances totalement injoignables, heureusement que ce n'étaient pas
celles de prod !

Au début j'ai simplement configuré /etc/network/interfaces de la façon
suivante afin d'utiliser dhcp pour IPv6:

    % cat /etc/network/interfaces# interfaces(5) file used by ifup(8) and ifdown(8)auto loiface lo inet loopbackauto eth0iface eth0 inet dhcpiface eth0 inet6 dhcp

Mais après un redémarrage mon instance de test n'arrivait pas à
configurer le réseau, et était donc injoignable et inutilisable. Après
quelques tests, j'ai réalisé que le problème venait du cient
[DHCP](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&cad=rja&uact=8&ved=0ahUKEwi3z73sz8nYAhVo5YMKHUcpCKUQFggwMAI&url=https%3A%2F%2Ffr.wikipedia.org%2Fwiki%2FDynamic_Host_Configuration_Protocol&usg=AOvVaw2S3dJH3qttc4OBiPoW6uxs)
installé, qui était [dhcpcd](https://packages.debian.org/wheezy/dhcpcd).
Apparemment le paquet installé sur mon système était une relique de
Debian 7, car il n'est pas disponible pour les versions ultérieures ! Je
l'ai donc remplacé par
[isc-dhcp-client](https://packages.debian.org/stretch/isc-dhcp-client).

    % sudo apt install isc-dhcp-client isc-dhcp-common% sudo apt remove dhcpcd

Après un redémarrage, tout fonctionne, mon instance obtient son adresse
IPv6 !

Articles: 

