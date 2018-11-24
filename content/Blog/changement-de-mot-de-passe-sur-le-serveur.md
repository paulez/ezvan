Title: Changement de mot de passe sur le serveur
Date: 2011-06-11 21:53
Author: Paul
Tags: Debian, LDAP, PAM, Services
Slug: changement-de-mot-de-passe-sur-le-serveur

Depuis la migration et l'utilisation d'un serveur LDAP pour gérer les
comptes des utilisateurs, il n'était plus possible de changer de mot de
passe avec passwd.

Le problème venait de la configuration par défaut de Debian Squeeze.
Dans le fichier /etc/pam/common-password, il faut remplacer :

password \[success=2 default=ignore\] pam\_unix.so obscure sha512  

password \[success=1 user\_unknown=ignore default=die\] pam\_ldap.so
use\_authtok try\_first\_pass  
</code>

par :

password \[success=2 default=ignore\] pam\_unix.so obscure sha512  

password \[success=1 user\_unknown=ignore default=die\] pam\_ldap.so
try\_authtok try\_first\_pass  
</code>


