Title: Let's Encrypt et Drupal 7
Date: 2018-08-19 01:29
Author: paul
Slug: lets-encrypt-et-drupal-7

<div
class="field field-name-body field-type-text-with-summary field-label-hidden">

<div class="field-items">

<div class="field-item even">

Le vieux certificat SSL fournit par Gandi pour
[www.ezvan.fr](https://www.ezvan.fr/) a expiré sans crier gare ! Je n’ai
pas accès au compte qui gère le domaine, me voilà donc en train
d’essayer de créer un certificat avec Let's Encrypt.  
[Let's Encrypt](https://letsencrypt.org/) est une autorité de
certification qui fournit des certificats SSL gratuits, donc plus aucune
excuse pour ne pas utiliser SSL correctement !  

La validation du certificat est faite automatiquement, à l’aide d’un
outil nommé cerbot. Il génère un fichier “ACME challenge” qui doit être
accessible via le domaine validé.  

Dans mon cas j’utilise la commande suivante. Je spécifie le chemin
d’installation de Drupal (qui fait tourner ce site) et demande à cerbot
de configurer Apache pour utiliser le nouveau certificat.

</p>
    % sudo certbot --authenticator webroot --installer apache --webroot -w /usr/share/drupal7 -d www.ezvan.fr

Malheureusement tout ne se passe pas comme prévu !

</p>
     - The following errors were reported by the server:   Domain: www.ezvan.fr   Type:   unauthorized   Detail: Invalid response from   http://www.ezvan.fr/.well-known/acme-challenge/UWXvHv0ueIHLLooJIcIfdD2OiuNipVF5TuSc0dXnXd0:   "      403 Forbidden      Forbidden"

Que se passe-t-il ? Drupal interdit l’accès direct aux fichiers placés
dans son arborescence pour des raisons de sécurité. L’emplacement du
fichier acme-challenge est standard ([RFC
5785](https://tools.ietf.org/html/rfc5785) mais la version 7 de Drupal
ne la prend pas en compte, et donc interdit l’accès.  

Heureusement je ne suis pas le seul à avoir eu ce problème, et il existe
déjà un [patch](https://www.drupal.org/project/drupal/issues/2847325)
pour autoriser l’accès à ce répertoire. Après avoir appliqué ce patch au
fichier .htaccess situé à la racine du répertoire Drupal, je peux
relancer la commande avec succès.

</p>
     - Congratulations! Your certificate and chain have been saved at   /etc/letsencrypt/live/www.ezvan.fr/fullchain.pem. Your cert will   expire on 2018-11-16. To obtain a new or tweaked version of this   certificate in the future, simply run certbot again with the   "certonly" option. To non-interactively renew *all* of your   certificates, run "certbot renew"

Et voilà mon certificat est configuré ! Je peux maintenant vérifier que
j’obtiens un score correct sur [le site SSL
Labs](https://www.ssllabs.com/ssltest/analyze.html?d=www.ezvan.fr).

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

[SSL](https://www.ezvan.fr/taxonomy/term/67)

</div>

<div class="field-item even">

[Web](https://www.ezvan.fr/taxonomy/term/39)

</div>

</div>

</div>

<div
class="field field-name-taxonomy-vocabulary-2 field-type-taxonomy-term-reference field-label-above">

<div class="field-label">

Articles: 

</div>

<div class="field-items">

<div class="field-item even">

[Linux](https://www.ezvan.fr/taxonomy/term/10)

</div>

<div class="field-item odd">

[Site](https://www.ezvan.fr/taxonomy/term/7)

</div>

</div>

</div>

</p>

