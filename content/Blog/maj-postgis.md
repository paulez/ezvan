Title: Mise à jour de PostGIS problématique et Fedora
Date: 2020-05-09 00:00
Author: Paul
Slug: maj-postgis
Lang: fr
Tags: PostgreSQL, Fedora, Libre, conteneurs

Pour quelques uns de mes projets de développement, j'utilise [PostGIS](https://postgis.net/), une extension de la base de données [PostgreSQL](https://www.postgresql.org/) qui permet de gérer des données géographiques. PostgreSQL et PostGIS sont régulièrement mises à jour, ce qui m'occasionne parfois de sacrés maux de tête. Danc cet article j’explique comment j’ai réussi à me sortir d’une mise à jour difficile à l’aide des outils fournis par Fedora et des conteneurs.

### Ciel, une mise à jour

Un changement de version majeure de PostgreSQL n'est pas une opération triviale, car elle nécessite toujours de convertir les bases de données du système, la compatibilité du schéma étant cassée entre chacune de versions majeures.

L'utilitaire [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) est utilisé pour cela, mais il est un peu compliqué à utiliser. Heureusement certaines distributions proposent des outils pour simplifier cette mise à jour. Par exemple sous Debian, la mise à jour du paquet d'une version majeure vers une autre entraîne une conversion automatique de la base de données.
Sous Fedora, ça n'est pas automatique, mais un utilitaire est fourni pour aider à la mise à jour.

Cela se complexifie avec PostGIS, comme on va le voir tout de suite.
J'ai donc récemment mis à jour ma [Fedora](https://getfedora.org/) de la version 31 vers la version 32.
Je décide de travailler un peu sur mon projet qui utilise PostGIS. Je tente de démarrer PostgreSQL.

```shell
% sudo systemctl start postgresql
```

### Les soucis commencent

Mais j'obtiens une erreur.

```
-- L'unité (unit) postgresql.service a commencé à démarrer.
mai 08 14:14:05 gen3 postgresql-check-db-dir[50660]: An old version of the database format was found.
mai 08 14:14:05 gen3 postgresql-check-db-dir[50660]: Use 'postgresql-setup --upgrade' to upgrade to version '12'
mai 08 14:14:05 gen3 postgresql-check-db-dir[50660]: See /usr/share/doc/postgresql/README.rpm-dist for more information.
mai 08 14:14:05 gen3 systemd[1]: postgresql.service: Control process exited, code=exited, status=1/FAILURE
-- Subject: Unit process exited
```

Fedora 31 fournit la version 11 de PostgreSQL, et Fedora 32 la version 12. Le schéma de la version 11 étant incompatible avec la version 12, je dois mettre à jour le format de la base de données. Je m’exécute donc à l’aide de l’utilitaire *postgresql-setup*.

```shell
% sudo postgresql-setup --upgrade
```

Mais j’obtiens une erreur !

```shell
pg_dump: erreur : échec de la requête : ERROR:  could not access file "$libdir/postgis-2.5": Aucun fichier ou dossier de ce type
pg_dump: erreur : la requête était : SELECT
```
Le problème est le suivant. L'utilitaire fait un dump de la base. Comme celle-ci utilise la version 2.5 de PostGIS, PostgreSQL doit utiliser cette même version pour réaliser le dump. Malheureusement la version 3.0 est installée sur le système, et donc PostgreSQL ne peut pas réaliser l’opération.

Il nous faut donc installer la version 2.5 de PostGIS. On peut essayer de trouver si cette version antérieure de PostGIS n’est pas fournie par un autre paquet ?

```
% dnf provides "*postgis-2.5"

postgis-upgrade-3.0.1-2.fc32.x86_64 : Support for upgrading from the previous major release of Postgis
Dépôt               : @System
Correspondances trouvées dans  :
Autre  : *postgis-2.5

postgis-upgrade-3.0.1-2.fc32.x86_64 : Support for upgrading from the previous major release of Postgis
Dépôt               : fedora
Correspondances trouvées dans  :
Autre  : *postgis-2.5
```
On voit en effet que cette version est fournie par le paquet *postgis-upgrade*. Pratique ! Installons-le et recommençons.

```shell
% sudo dnf install postgis-upgrade
% sudo postgresql-setup --upgrade
```

### De pire en pire

L’erreur initiale n’est plus là, mais cela échoue de nouveau, avec une erreur encore plus cryptique !

```shell
pg_restore: error: could not execute query: ERROR:  column s.consrc does not exist
LINE 28:             "replace"("split_part"("s"."consrc", ''''::"text...
                                            ^
HINT:  Perhaps you meant to reference the column "s.conkey" or the column "s.conbin".
```

Après quelques recherches, je réalise que c'est dû à un changement de schéma dans PostgreSQL, et que la solution est de mettre à jour PostGIS avant de mettre à jour PostgreSQL. Oui mais comment faire alors que je n’ai plus l’ancienne version de disponible ?

### Les conteneurs à la rescousse

Une solution serait de lancer un conteneur de la version précédente de Fedora, d’y attacher le répertoire contenant les bases de données PostgreSQL, et d’y réaliser la mise à jour du module PostGIS.

Pour cela j’utilise [podman](https://podman.io/) de la façon suivante.

```shell
% sudo podman run -it --name pgsql-upgrade --rm --volume /var/lib/pgsql/:/var/lib/pgsql/ --security-opt label=disable fedora:31 bash
```

L'option *security-opt* permet au conteneur d'accéder au répertoire */var/lib/pgsql* qui sinon serait bloqué par SELinux.

J'installe les paquet nécessaires.

```
# dnf install -y postgresql-server postgis
```

Il me faut une version plus récente de PostGIS que celle fournie dans Fedora 31 (2.5.1). J’ai de la chance, la version 2.5.4 est disponible sur [Koji](https://koji.fedoraproject.org/koji/packageinfo?packageID=4681), le système de construction de paquets de Fedora.

Je la télécharge donc et l’installe.

```
# curl https://kojipkgs.fedoraproject.org//packages/postgis/2.5.4/1.fc31/x86_64/postgis-2.5.4-1.fc31.x86_64.rpm -o postgis-2.5.4-1.fc31.x86_64.rpm

# dnf install postgis-2.5.4-1.fc31.x86_64.rpm
```

Nouvelle astuce, il me faut installer les données de langue supplémentaires du système, car sinon le client psql va refuser de se connecter à ma base de données qui utilise la locale fr_FR.UTF-8.

```
# dnf -y swap glibc-minimal-langpack glibc-all-langpacks
```

Je change ensuite d’utilisateur vers l’utilisateur système utilisé par PostgreSQL.

```
# su - postgres
```

Je dois éditer la configuration du serveur PostgreSQL qui contient des entrées qui bloquent le démarrage de la base car certaines locales sont toujours manquantes sur le système.

```shell
% cp /var/lib/pgsql/data/postgresql.conf /var/lib/pgsql/data/postgresql.conf.0
```

Je démarre le serveur de base de données.

```shell
% pg_ctl -D /var/lib/pgsql/data/ start
```

Je me connecte à la base à corriger, et je mets à jour l’extension postgis. À noter qu’il faut faire cette opération pour chaque base qui utilise PostGIS.

```
% psql yourdb
ALTER EXTENSION postgis update;
\q
```

J'arrête le serveur et je restaure la configuration d'origine.

```shell
% pg_ctl -D /var/lib/pgsql/data/ stop
% cp /var/lib/pgsql/data/postgresql.conf.0 /var/lib/pgsql/data/postgresql.conf
```

### Tout est bien qui finit bien

Je quitte mon conteneur. Je peux de nouveau lancer l’utilitaire de mise à jour de la base, cette fois avec succès !

```shell
% sudo postgresql-setup --upgrade
% sudo systemctl start postgresql
```

```
-- L'unité (unit) postgresql.service a commencé à démarrer.
mai 08 17:45:11 gen3 postmaster[200071]: 2020-05-08 17:45:11.174 CEST [200071] LOG:  démarrage de PostgreSQL 12.2 on x86_64-redhat-linux-gnu, co>
mai 08 17:45:11 gen3 postmaster[200071]: 2020-05-08 17:45:11.174 CEST [200071] LOG:  en écoute sur IPv6, adresse « ::1 », port 5432
mai 08 17:45:11 gen3 postmaster[200071]: 2020-05-08 17:45:11.174 CEST [200071] LOG:  en écoute sur IPv4, adresse « 127.0.0.1 », port 5432
mai 08 17:45:11 gen3 postmaster[200071]: 2020-05-08 17:45:11.178 CEST [200071] LOG:  écoute sur la socket Unix « /var/run/postgresql/.s.PGSQL.54>
mai 08 17:45:11 gen3 postmaster[200071]: 2020-05-08 17:45:11.182 CEST [200071] LOG:  écoute sur la socket Unix « /tmp/.s.PGSQL.5432 »
mai 08 17:45:11 gen3 postmaster[200071]: 2020-05-08 17:45:11.196 CEST [200071] LOG:  redirection des traces vers le processus de récupération de>
mai 08 17:45:11 gen3 postmaster[200071]: 2020-05-08 17:45:11.196 CEST [200071] ASTUCE :  Les prochaines traces apparaîtront dans le répertoire «>
mai 08 17:45:11 gen3 systemd[1]: Started PostgreSQL database server.
-- Subject: L'unité (unit) postgresql.service a terminé son démarrage
```

### Le mot de la fin

Pour conclure, on peut noter que la mise à jour d'une base de données est une opération délicate, même sur une machine de développement !

Les conteneurs sont un outil efficace afin de pouvoir utiliser une version différente du système et corriger des potentielles erreurs avant la migration. Le paquet *postgis-upgrade* est aussi nécessaire pour réaliser une mise à jour d’une base de données PostGIS sous Fedora.
