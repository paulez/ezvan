Title: Reconstruire le menu d'administration de Drupal
Date: 2015-06-01 15:32
Author: Paul Ezvan
Slug: reconstruire-le-menu-dadministration-de-drupal

<div
class="field field-name-body field-type-text-with-summary field-label-hidden">

<div class="field-items">

<div class="field-item even">

J'avais des soucis avec mes pages d'administration de Drupal, certaines
m'affichaient l'erreur "Vous n'avez accès à aucune page
d'administration." Cette erreur est survenue après la mise à jour de
Drupal 6 vers la version 7.

</p>
J'ai pu corriger ce problème en reconstruisant les liens d'aministration
en utilisant la requête SQL suivante sur la base de données de Drupal:

</p>
`DELETE FROM menu_links WHERE module = 'system'`

</p>
Ensuite il suffit de se rendre sur /admin/config/development/performance
et de nettoyer le cache.

</p>
Pour finir je n'avais plus qu'à rajouter le bloc du menu dans la barre
latérale pour obtenir un menu d'administration tout neuf.

</p>
 

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

[Drupal](https://www.ezvan.fr/taxonomy/term/57)

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

[Logiciels](https://www.ezvan.fr/taxonomy/term/6)

</div>

</div>

</div>

</p>

