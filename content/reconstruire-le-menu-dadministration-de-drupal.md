Title: Reconstruire le menu d'administration de Drupal
Date: 2015-06-01 15:32
Author: Paul
Tags: Drupal, Logiciels
Slug: reconstruire-le-menu-dadministration-de-drupal

J'avais des soucis avec mes pages d'administration de Drupal, certaines
m'affichaient l'erreur "Vous n'avez accès à aucune page
d'administration." Cette erreur est survenue après la mise à jour de
Drupal 6 vers la version 7.

J'ai pu corriger ce problème en reconstruisant les liens d'aministration
en utilisant la requête SQL suivante sur la base de données de Drupal:

`DELETE FROM menu_links WHERE module = 'system'`

Ensuite il suffit de se rendre sur /admin/config/development/performance
et de nettoyer le cache.

Pour finir je n'avais plus qu'à rajouter le bloc du menu dans la barre
latérale pour obtenir un menu d'administration tout neuf.

Articles: 

