Title: Problème avec le téléversement automatique de Nextcloud
Date: 2018-03-05 12:14
Author: Paul
Tags: Libre, Nextcloud
Slug: probleme-avec-le-televersement-automatique-de-nextcloud

Depuis quelques jours la fonctionnalité de téléversement automatique de
Nextcloud qui me permet d’envoyer automatiquement mes photos depuis mon
téléphone Android échouait sans cesse avec une erreur:

    Impossible de réaliser l’opération: le serveur n’est pas accessible

Cette erreur est un peu étrange car le reste de l’application fonctionne
parfaitement. En fait elle est causée par un bogue dans la version 3.0.2
du client Android qui ne crée pas automatiquement de nouveau dossier
pour le mois en cours quand vous choisissez de classer les photos par
mois.

Pour résoudre temporairement ce problème il suffit de créer le dossier
pour le mois en cours (nommé **03** pour mars) dans le répertoire
d’envoi via l’interface web. Vous pouvez trouver plus d’information sur
le problème dans le [ticket Github
correspondant](https://github.com/nextcloud/android/issues/2249).

