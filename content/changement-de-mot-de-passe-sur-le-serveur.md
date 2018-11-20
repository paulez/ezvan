Title: Changement de mot de passe sur le serveur
Date: 2011-06-11 21:53
Author: Paul Ezvan
Slug: changement-de-mot-de-passe-sur-le-serveur

<div
class="field field-name-body field-type-text-with-summary field-label-hidden">

<div class="field-items">

<div class="field-item even">

Depuis la migration et l'utilisation d'un serveur LDAP pour gérer les
comptes des utilisateurs, il n'était plus possible de changer de mot de
passe avec passwd.

</p>
Le problème venait de la configuration par défaut de Debian Squeeze.
Dans le fichier /etc/pam/common-password, il faut remplacer :

</p>
password \[success=2 default=ignore\] pam\_unix.so obscure sha512  

password \[success=1 user\_unknown=ignore default=die\] pam\_ldap.so
use\_authtok try\_first\_pass  
</code>

</p>
par :

</p>
password \[success=2 default=ignore\] pam\_unix.so obscure sha512  

password \[success=1 user\_unknown=ignore default=die\] pam\_ldap.so
try\_authtok try\_first\_pass  
</code>

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

[Debian](https://www.ezvan.fr/taxonomy/term/27)

</div>

<div class="field-item odd">

[LDAP](https://www.ezvan.fr/taxonomy/term/29)

</div>

<div class="field-item even">

[PAM](https://www.ezvan.fr/taxonomy/term/30)

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

[Services](https://www.ezvan.fr/taxonomy/term/8)

</div>

</div>

</div>

</p>

