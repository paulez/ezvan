Title: Changer la taille de police dans les applications Qt sous Xfce
Date: 2020-05-25 19:00
Author: Paul
Tags: Linux, Libre, Astuces
Slug: taille-police-qt
Lang: fr

En ce moment j’utilise [Xfce](https://xfce.org/) comme environnement de bureau, pour soulager mon ordinateur portable âgé de sept ans qui fatigue un peu.

Comme je suis myope, je change toujours la taille des polices en changeant le [DPI](https://fr.wikipedia.org/wiki/Point_par_pouce), pour le régler à 120. C’est facile à faire dans Xfce en utilisant le module « Apparence » du panneau de paramètres.

Mais dans certaines applications qui utilisent le [framework Qt](https://www.qt.io/) ce paramètre n’était pas toujours respecté. Après quelques recherches, j’ai trouvé qu’un moyen simple de changer l’apparence dans ces applications est d’utiliser le fichier *~/.Xresources*. Ce fichier est utilisé par le [serveur X](https://fr.wikipedia.org/wiki/X_Window_System) pour configurer ses applications clientes.

Voici la configuration que j’ai utilisée :

```
!-------------------------------------------------------------------------------
! Xft settings
!-------------------------------------------------------------------------------

Xft.dpi:        120
Xft.antialias:  true
Xft.rgba:       rgb
Xft.hinting:    true
Xft.hintstyle:  hintslight
Xft.autohint:   false
Xft.lcdfilter:  lcddefault
```
Il faut ensuite utiliser la commande *xrdb* pour appliquer ces paramètres :

```shell
xrdb -merge ~/.Xresources
```

Et voilà, mes applications Qt comme [KeepassXC](https://keepassxc.org/) ont la bonne taille de police !
