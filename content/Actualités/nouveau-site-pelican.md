Title: Nouveau site avec Pelican
Author: Paul
Tags: Services, Site, Pelican, Libre
Slug: nouveau-site-pelican
Lang: fr
Date: 2018-11-24 22:00
Summary: Je viens de publier une nouvelle version du site. J'en ai profité pour ré-organiser le site et utiliser un thème un peu plus moderne.

Je viens de publier une nouvelle version du site. J'en ai profité pour ré-organiser le site et utiliser un thème un peu plus moderne.

## Changement de plate-forme

À cette occasion je dis au revoir à Drupal pour Pelican. 

### Drupal à la retraite

Pourquoi ce choix ? [Drupal](https://www.drupal.org/) est assez compliqué à configurer, et aussi à migrer vers une nouvelle version. La version que j'utilisais est la version 7 qui commence à dater, ce qui se ressent dans l'aspect un peu vieillot. Mettre à jour vers la version 8 aurait nécessité pas mal de travail, autant investir ce temps dans une autre solution !

De plus j'avais pas mal de problèmes avec le spam, que ça soit pour les commentaires ou l'inscription d'utilisateurs. J'ai configuré divers modules d'antispam, mais je reçois toujours une quantité incroyable de commentaires écrits en cyrilliques et d'inscriptions d'utilisateurs avec des addresses mail bidon.

Finalement, l'aspect sécurité est aussi à prendre en compte. Heureusement j'utilise [le paquet fournit par Debian pour Drupal 7](https://packages.debian.org/stretch/drupal7), ce qui signifie que la formidable équipe de [Debian](https://www.debian.org/) s'occupe des mises à jour de sécurité pour moi. Mais il y a toujours un risque de faille inconnue ou dite "0-day" pouvant mener à la compromission du site. Une bonne raison pour utiliser un site statique !

### Pelican se pose

[Pelican](http://docs.getpelican.com/) est un générateur de site statique. Il permet de générer un site complet simplement à partir de quelques paramètres et de contenu stocké dans des fichiers textes. C'est une grosse différence de concept avec Drupal qui est de type "[CMS](https://fr.wikipedia.org/wiki/Syst%C3%A8me_de_gestion_de_contenu)", c'est à dire un logiciel dynamique qui génère le contenu à la volée à partir de données stockées dans une base de données. Le site est généré une seule fois, au lieu de l'être à chaque visite.

### Dr. Jekyll

Il existe de nombreuses autres générateurs de sites statiques, dont pour citer certains connus, [Jekyll](https://jekyllrb.com/), [Hugo](https://gohugo.io/), etc.
Pourquoi l'un et pas l'autre ? 
J'ai commencé par tester [Hugo](https://gohugo.io/), mais j'ai eu quelques difficultés à le faire fonctionner sur [Debian Stretch](https://wiki.debian.org/fr/DebianStretch), entre version de [Go](https://golang.org/) trop vieille et problème de dépendance.

J'ai ensuite essayé [Pelican](http://docs.getpelican.com/) car il est disponible dans [Debian Stretch](https://wiki.debian.org/fr/DebianStretch), et écrit en [Python](https://fr.wikipedia.org/wiki/Python_(langage)) ce qui me facilite la tâche pour résoudre des potentiels problèmes. Étant rapidement parvenu à un résultat honorable, je ne suis pas aller fouiller ailleurs !

La plupart des générateurs utilisent un concept similaire à base de fichiers au [format Markdown](https://fr.wikipedia.org/wiki/Markdown). Il semble donc aisé de migrer d'une solution à l'autre, le choix n'en est que plus simple.

## Ce qui change

Pages statiques obligent, le fonctionnement du site est quelque peu différent.

### Commentaires

Il n'y a plus de commentaires. Finis, disparus. Ceux-ci étaient utilisées en écrasante majorité par des spammeurs de tous poils, la perte devrait être minime. 
Il existe des solutions comme utiliser [Disqus](https://disqus.com/), mais je suis modérément enthousiaste à l'idée d'ajouter un traceur publicitaire à ce site.

Vous pouvez toujours m'envoyer un message via [la page de contact]({filename}/pages/contact.md) pour commenter un article !

### Écrire un article

Il n'est également plus possible d'écrire un article directement depuis le site.

Pour publier un article envoyez le moi via [la page de contact]({filename}/pages/contact.md) ou créez une "pull request" sur [le projet Github](https://github.com/paulez/ezvan).

Les articles sont formatés à l'aide de [Markdown](https://fr.wikipedia.org/wiki/Markdown). [Le fichier source de l'article précédent](https://raw.githubusercontent.com/paulez/ezvan/master/content/Blog/lets-encrypt-et-drupal-7.md) peut servir d'exemple.

## Comment ça marche

J'utilise la version de Pelican fournie avec Debian, que j'ai installé à l'aide de la commande `apt install pelican`.

Après avoir créé un projet en utilisant `pelican-quickstart`, j'ai importé les articles existant sur du site en lançant `pelican-import --feed  https://www.ezvan.fr/rss.xml -o output/ -m markdown`.

Certaines choses sont manquantes comme les étiquettes des articles, et le résultat comporte du code HTML superflu. Pour nettoyer un peu tout ça j'ai écrit [un script de conversion](https://github.com/paulez/ezvan/blob/master/convert.py).

Après avoir réorganisé le contenu on peut tester le résultat dans un navigateur en lançant la commande `make devserver` et en visitant [http://localhost:8000](http://localhost:8000).

Pelican fournit une configuration [Fabric](http://www.fabfile.org/) qui permet d'automatiser le déploiement. 
Après avoir installé Fabric avec `sudo apt install fabric` et avoir configuré [fabfile.py](https://github.com/paulez/ezvan/blob/master/fabfile.py), je peux simplement déployer. Il suffit d'invoquer Fabric en lançant `fab publish`.

J'ai publié l'ensemble des sources du site sur [mon dépôt GitHub](https://github.com/paulez/ezvan).

## Références

* Un article sur Pelican dans GLMF: [Utiliser Pelican comme moteur de blog](https://connect.ed-diamond.com/GNU-Linux-Magazine/GLMF-184/Utiliser-Pelican-comme-moteur-de-blog)
* La documentation de Pelican: [Quickstart](http://docs.getpelican.com/en/3.7.1/quickstart.html)
* Blog narrant une migration de Drupal vers Pelican: [Transitioning from Drupal to Pelican ](https://www.graham.org/pelican-transition.html)
* Guide de création de site avec Pelican: [How to set up a Pelican static blog site](https://blog.john-pfeiffer.com/how-to-set-up-a-pelican-static-blog-site/#importing-from-drupal-with-pelican-import)