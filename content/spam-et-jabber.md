Title: Spam et Jabber
Date: 2012-05-03 21:11
Author: Paul Ezvan
Slug: spam-et-jabber
Category: Site
Tags: Jabber, Spam, ejabberd, Libre

Le spam est un problème récurrent sur les services que j'administre sur
[ezvan.fr](http://www.ezvan.fr).

Que ça soit pour le serveur de courrier, le site web, le serveur
[Jabber](http://fr.wikipedia.org/wiki/Extensible_Messaging_and_Presence_Protocol)...
Tous sont envahis de requêtes de robots tentant d'inonder ce petit bout
d'Internet de publicité, d'arnaque ou autre message malfaisant.

Récemment j'ai remarqué que certains utilisateurs du serveur de
messagerie instantanée Jabber faisaient un nombre un peu élevé de
requêtes. Après étude il semblait que ceux-ci s'attelaient à bombarder
d'autres serveurs de messagerie. Plus de dix mille utilisateurs étaient
alors inscrits sur le serveur, avec le plus souvent des noms générés
automatiquement.

Après avoir nettoyé du mieux que possible ces utilisateurs, en
supprimant ceux ayant des noms trop évidents et ceux sans connexion
depuis plus de cent jours, je me suis attelé à limiter le nombre de
robot s'inscrivant dessus. Depuis peu le serveur utilisé pour ce
service, [ejabberd](http://www.ejabberd.im/), permet de demander à
l'utilisateur de répondre à une question de type
[Captcha](http://fr.wikipedia.org/wiki/Captcha) pour utiliser certaines
fonctions. J'ai activé cette fonctionnalité pour l'inscription des
nouveaux utilisateurs.

Je sais que ce système n'est pas parfait car il peut être contourné par
ces robots et présenter des problèmes d'accessibilité, mais je n'ai pas
trouvé de meilleur moyen pour réduire ce problème. Peut-être qu'un
lecteur connaîtrait une meilleure approche ? N'hésitez pas à m'en faire
part si vous avez des difficultés à vous inscrire sur le serveur.

