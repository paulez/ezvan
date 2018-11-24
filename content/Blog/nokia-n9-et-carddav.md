Title: Nokia N9 et CardDav
Date: 2012-07-21 14:55
Author: Paul
Tags: Logiciel, N9, CardDav, Libre
Slug: nokia-n9-et-carddav

Je viens d'acquérir le Nokia N9, le dernier smartphone sorti par Nokia
avant le pacte avec Microsoft. Il utilise le système Meego Harmattan.

Comme [vous le savez déjà](https://www.ezvan.fr/node/62), j'utilise les
protocoles CalDav et CardDav pour synchroniser mes contacts et mon
agenda, le tout hébergé sur ezvan.fr. De base le système du N9 propose
une synchronisation Caldav (pour le calendrier) mais par CardDav.

Voici donc comment j'ai mis en place une telle synchronisation, à l'aide
de [SyncEvolution](https://syncevolution.org/).

Tout d'abord, j'ai récupéré [un paquet .deb de
SyncEvolution](http://www.ezvan.fr/public/logiciels/n9/syncevolution_1.2.2-1_armel.deb)
compilé avec le support de CardDav. Après l'avoir installé avec la
commande dpkg, j'ai lancé les commandes suivantes pour configurer mon
compte CardDav, remplacez &lt;utilisateur&gt; et &lt;motdepasse&gt; par
le mot idoine.

```
# configure target config for CardDAVsyncevolution --configure \
             --template webdav \
             syncURL=https://cal.ezvan.fr/<utilisateur>/contacts/ \
             SSLVerifyServer=0 \
             username=<utilisateur> \
             password=<motdepasse> \
             target-config@carddav \
             addressbook

# configure sync config for CardDAV  
syncevolution --configure \\  
              --template SyncEvolution\_Client \\  
              syncURL=local://@carddav \\  
              username= \\  
              password= \\  
              carddav \\  
              addressbook

# initial slow sync for CardDAV  
syncevolution --sync slow carddav

# incremental sync for CardDAV  
syncevolution carddav
```

Et ça marche ! Il ne me reste plus qu'à trouver comment lancer la
commande de synchronisation à intervalle de temps régulier.

