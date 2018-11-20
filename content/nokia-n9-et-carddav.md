Title: Nokia N9 et CardDav
Date: 2012-07-21 14:55
Author: paul
Slug: nokia-n9-et-carddav

<div
class="field field-name-body field-type-text-with-summary field-label-hidden">

<div class="field-items">

<div class="field-item even">

Je viens d'acquérir le Nokia N9, le dernier smartphone sorti par Nokia
avant le pacte avec Microsoft. Il utilise le système Meego Harmattan.

</p>
Comme [vous le savez déjà](https://www.ezvan.fr/node/62), j'utilise les
protocoles CalDav et CardDav pour synchroniser mes contacts et mon
agenda, le tout hébergé sur ezvan.fr. De base le système du N9 propose
une synchronisation Caldav (pour le calendrier) mais par CardDav.

</p>
Voici donc comment j'ai mis en place une telle synchronisation, à l'aide
de [SyncEvolution](https://syncevolution.org/).

</p>
Tout d'abord, j'ai récupéré [un paquet .deb de
SyncEvolution](http://www.ezvan.fr/public/logiciels/n9/syncevolution_1.2.2-1_armel.deb)
compilé avec le support de CardDav. Après l'avoir installé avec la
commande dpkg, j'ai lancé les commandes suivantes pour configurer mon
compte CardDav, remplacez &lt;utilisateur&gt; et &lt;motdepasse&gt; par
le mot idoine.

</p>
`# configure target config for CardDAVsyncevolution --configure \             --template webdav \             syncURL=https://cal.ezvan.fr/<utilisateur>/contacts/ \             SSLVerifyServer=0 \             username=<utilisateur> \             password=<motdepasse> \             target-config@carddav \             addressbook`

</p>
\# configure sync config for CardDAV  
syncevolution --configure \\  
              --template SyncEvolution\_Client \\  
              syncURL=local://@carddav \\  
              username= \\  
              password= \\  
              carddav \\  
              addressbook

</p>
\# initial slow sync for CardDAV  
syncevolution --sync slow carddav

</p>
\# incremental sync for CardDAV  
syncevolution carddav

</p>
Et ça marche ! Il ne me reste plus qu'à trouver comment lancer la
commande de synchronisation à intervalle de temps régulier.

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

[Logiciel](https://www.ezvan.fr/taxonomy/term/42)

</div>

<div class="field-item odd">

[N9](https://www.ezvan.fr/taxonomy/term/46)

</div>

<div class="field-item even">

[CardDav](https://www.ezvan.fr/taxonomy/term/47)

</div>

<div class="field-item odd">

[Libre](https://www.ezvan.fr/taxonomy/term/48)

</div>

</div>

</div>

</p>

