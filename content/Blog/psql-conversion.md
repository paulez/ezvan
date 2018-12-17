Title: Conversion de type avec PostgreSQL
Date: 2018-12-16 19:00
Author: Paul
Slug: psql-conversion
Lang: fr
Tags: PostgreSQL, Libre, Roundcube

Tous les jours je reçois un message d'erreur généré par le script cron de mon logiciel de webmail Roundcube:

```
ERROR: [7] ERROR:  operator does not exist: boolean = integer
LINE 1: DELETE FROM "contactgroups" WHERE "del" = 1 AND "changed" < ...
                                                ^
HINT:  No operator matches the given name and argument type(s). You might need to
 add explicit type casts. (SQL Query: DELETE FROM "contactgroups" WHERE "del" = 1
  AND "changed" < '2018-12-04 00:00:00')
```

Il semble que l'erreur soit causée par une incompatibilité entre le schéma de la base de données et la requête SQL utilisée par le script de nettoyage.

Pour administrer mes bases de données PostgreSQL simplement j'utilise le logiciel web [phpPgAdmin](http://phppgadmin.sourceforge.net/doku.php). En observant le schéma de la table **contactgroups** je note que le type de la colonne **del** est *boolean*. C'est incompatible avec la requête `DELETE FROM "contactgroups" WHERE "del" = 1` car **del** devrait être un nombre entier (un *int*). PostreSQL est tâtillon avec les types, et ne convertit pas un entier en booléen implicitement, ce qui cause l'erreur.

J'avais importé cette base depuis MySQL vers PostgreSQL, ce qui a pu causer quelques incohérences avec la schéma attendu par Roundcube. Je vérifie que c'est le cas en comparant avec [le schéma fourni par Roundcube pour créer une base](https://github.com/roundcube/roundcubemail/blob/master/SQL/postgres.initial.sql) :

```
CREATE TABLE contactgroups (
    contactgroup_id integer DEFAULT nextval('contactgroups_seq'::text) PRIMARY KEY,
    user_id integer NOT NULL
        REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    changed timestamp with time zone DEFAULT now() NOT NULL,
    del smallint NOT NULL DEFAULT 0,
    name varchar(128) NOT NULL DEFAULT ''
);
```

En effet dans ce schéma la colonne **del** est de type *smallint*. Je vais donc modifier le schéma de la table pour utiliser le type *smallint* à la place de *boolean* à l'aide du client **psql**.

```
roundcube=> ALTER TABLE "public"."contactgroups" ALTER COLUMN "del" TYPE smallint;
ERROR:  column "del" cannot be cast automatically to type smallint
ASTUCE : You might need to specify "USING del::smallint".
```

Malheureusement la conversion échoue ! En effet PostgreSQL ne sait pas comment convertir un booléen en entier.

On peut donc lui indiquer:

```
roundcube=> ALTER TABLE "public"."contactgroups"
roundcube-> ALTER COLUMN "del" TYPE smallint
roundcube-> USING CASE WHEN del=FALSE then 0
roundcube-> WHEN del=TRUE then 1
roundcube-> else NULL
roundcube-> END;
ERROR:  default for column "del" cannot be cast automatically to type smallint
```

Nouvelle erreur ! Cette fois c'est la valeur par défaut du champ, configurée à FALSE, qui ne peut pas être convertie. Le plus simple est de supprimer la valeur par défaut, effectuer la conversion, puis rajouter une valeur par défaut.

```
roundcube=> ALTER TABLE "public"."contactgroups" ALTER COLUMN "del" DROP DEFAULT;
ALTER TABLE
roundcube=> ALTER TABLE "public"."contactgroups"                                 
ALTER COLUMN "del" TYPE smallint          
USING CASE WHEN del=FALSE then 0
WHEN del=TRUE then 1
else NULL
END;
ALTER TABLE
roundcube=> ALTER TABLE "public"."contactgroups" ALTER COLUMN "del" SET DEFAULT 0;
ALTER TABLE
```

Et voilà, pas de problème cette fois !

Modifier le schéma d'une base de données peut amener à se soucier de nombreuses subtilités. Ces opérations sont délicates et il vaut mieux toujours tester avant de réaliser ce type d'opération en production.