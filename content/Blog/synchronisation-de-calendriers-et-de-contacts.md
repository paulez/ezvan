Title: Synchronisation de calendriers et de contacts
Date: 2011-02-20 16:27
Author: Paul
Tags: Debian, Hébergement, CardDav, Libre, CalDav
Slug: synchronisation-de-calendriers-et-de-contacts
Lang: fr

Vendredi dernier, j'ai complétement oublié une réunion. Honte à moi ! Ce
petit imprévu m'a fait réaliser qu'il me fallait absoluement une
solution pour gérer mon calendrier. J'ai donc cherché comment réaliser
cela, avec les contraintes suivantes :

-   Utilisable avec de nombreux clients pour être accessible de partout,
    la liste de clients de test étant la suivante :

    </p>
    -   Evolution (groupware sous Linux que j'utilise)
    -   Korganizer (un autre)
    -   Un webmail comme Horde ou Roundcube
    -   Iphone (oui c'est mon téléphone pro)
-   Libre
-   Déployable sur ezvan.fr
-   Ne pas être une usine à gaz

Bien sûr ces critères éliminent les services de Google et consorts. Pas
mal de groupware répondent à la plupart des critères, mais généralement
ce sont des usines à gaz qui en font trop pour ce que je veux, et qui
imposent leur solution de messagerie, et il est hors de question de
remplacer la solution de mail actuelle. J'ai donc trouvé un serveur
plutôt léger, qui permet de synchroniser des calendriers avec le
protocol CalDav, et des contacts avec le protocol CardDav, c'est
[DAViCal](http://www.davical.org/).

Les format utilisés, sont comme l'indiquent les noms de protocoles, les
formats iCal (créé par Apple, bouh) et vCard. Ces formats me semblent
assez bien supportés par les clients sous Linux (Evolution, Mozilla,
Korganizer, Iphone et même Outlook !). Malheureusement les webmails
déployés sur ezvan.fr ne semblent pas le supporter pour l'instant. Enfin
c'est la solution la plus universelle que j'ai pu trouver.

### Installation

Passons maintenant aux étapes d'installation, réalisée sous Debian.
Premièrement il faut installer le serveur davical,
`aptitude install davical`. Pas trop dur !

Ensuite il faut une base de données PostgreSQL, seul type de base
supporté par davical. `aptitude install postgresql`. Un serveur Apache
doit être également présent et fonctionnel pour accéder à l'interface
web de davical. La base doit être configurée pour être accessible. Il
faut ajouter les lignes suivantes au début du fichier
/etc/postgresql/8.4/main/pg\_hba.conf :

`# davical local davical davical_app trust local davical davical_dba trust `

À noter que ces directives autorisent n'importe quel utilisateur local à
accéder aux bases davical, il faudrait donc affiner un peu !

Ensuite le script de création de la base doit être exécuté avec
l'utilisateur ayant les droits d'administration sur la base PostgreSQL,
en l'occurence postgres : ` `

`su postgres -c /usr/share/davical/dba/create-database.sh `

Ensuite il faut permettre l'accès à l'interface web de davical dans
Apache, en créant le fichier /etc/apache2/conf.d/davical.conf contenant
:

`Alias /davical /usr/share/davical/htdocs/  `

`Options +FollowSymLinks `

`AllowOverride All `

`order allow,deny `

`allow from all `

`AcceptPathInfo On `

`php_value include_path /usr/share/awl/inc `

`php_value magic_quotes_gpc 0 `

`php_value register_globals 0 `

`php_value error_reporting "E_ALL & ~E_NOTICE" `

`php_value default_charset "utf-8"  `

Et voilà, ça marche ! Je peux me connecter à l'interface de davical à
l'adresse http://hostname/davical avec les identifiants fournis par le
script d'installation, et ajouter des utilisateurs.

Le calendrier home (ressource créée par défaut) de l'utilisateur paul
est alors accessible à l'adresse
htt://hostname/davical/caldav.php/paul/home. L'adresse n'est pas simple
à rentrer par l'utilisateur, et nécessite pour un utilisateur d'Iphone
d'utiliser les paramétres avancés, il faut donc améliorer ça !

### Configuration

On veut donc que le calendrier home de l'utilisateur paul soit
accessible à l'adresse http://hostname/paul/home, et que le serveur
écoute sur les ports 8443 et 8008 en plus des ports standards pour que
l'Iphone ne pose pas plus de questions que l'utilisateur, le mot de
passe et le nom du site.

Pour changer l'adresse on utilise des règles de réécritures d'url, tout
cela dans un hôte virtuel Apache, qui sera accessible via
http://cal.ezvan.fr.

Sous Debian, on crée pour cela un fichier
/etc/apache2/sites-available/cal qui contient :

` DocumentRoot /usr/share/davical/htdocs `

`DirectoryIndex index.php index.html `

`ServerName cal.ezvan.fr `

`ServerAlias cal.ezvan.fr  `

`AllowOverride None `

`Order allow,deny `

`Allow from all  `

`Alias /images/ /usr/share/davical/htdocs/images/ `

`php_value include_path /usr/share/awl/inc php_value magic_quotes_gpc 0 php_value register_globals 0 `

`RewriteEngine On `

`# Not if it's the root URL. You might want to comment this out if you `

`# want to use an explicit /index.php for getting to the admin pages. `

`RewriteCond %{REQUEST_URI} !^/$ `

`# Not if it explicitly specifies a .php program, stylesheet or image `

`RewriteCond %{REQUEST_URI} !\.(php|css|js|png|gif|jpg) `

`# Everything else gets rewritten to /caldav.php/... `

`RewriteRule ^(.*)$ /caldav.php/$1 [NC,L]  `

Les premières directives correspondent à la configuration du nom de
l'hôte virtuel et à sa racine sur le disque dur. Ensuite est configuré
le module de réécriture d'URL afin de pouvoir avoir des URLs de la forme
/paul/home réécrites en /caldav.php/paul/home.

De même pour la version SSL, on crée un fichier ssl-cal. Attention, j'ai
du utiliser un nom classé alphabétiquement après default-ssl (le nom de
l'hôte virtuel ssl par défaut) sinon tous mes sites ssl étaient
redirigés vers davical, alors que dans cet ordre tout fonctionne
parfaitement (je n'ai pas trop compris pourquoi). Une piste se trouve
dans [le wiki
d'Apache](http://wiki.apache.org/httpd/NameBasedSSLVHosts).

`  # SSL Engine Switch: `

`# Enable/Disable SSL for this virtual host. `

`SSLEngine on `

`# A self-signed (snakeoil) certificate can be created by installing `

`# the ssl-cert package. See `

`# /usr/share/doc/apache2.2-common/README.Debian.gz for more info. `

`# If both key and certificate are stored in the same file, only the `

`# SSLCertificateFile directive is needed. `

`SSLCertificateFile /etc/ssl/private/server.crt `

`SSLCertificateKeyFile /etc/ssl/private/server.key `

`ServerName cal.ezvan.fr `

`ServerAlias cal.ezvan.fr `

`DocumentRoot /usr/share/davical/htdocs `

`DirectoryIndex index.php index.html  `

`AllowOverride None `

`Order allow,deny `

`Allow from all  `

`Alias /images/ /usr/share/davical/htdocs/images/ `

`php_value include_path /usr/share/awl/inc `

`php_value magic_quotes_gpc 0 `

`php_value register_globals 0 `

`RewriteEngine On `

`# Not if it's the root URL. You might want to comment this out if you `

`# want to use an explicit /index.php for getting to the admin pages. `

`RewriteCond %{REQUEST_URI} !^/$ `

`# Not if it explicitly specifies a .php program, stylesheet or image `

`RewriteCond %{REQUEST_URI} !\.(php|css|js|png|gif|jpg) `

`# Everything else gets rewritten to /caldav.php/... `

`RewriteRule ^(.*)$ /caldav.php/$1 [NC,L]   `

Par rapport au fichier précédent se trouvent les paramètres de
configuration de SSL.

Attention encore ! Pour avoir plusieurs hôtes virtuels écoutant sur la
même adresse, il faut changer quelques directives par défaut dans la
conf Apache de Debian. Dans le fichier /etc/apache2/ports.conf, il faut
rajouter `NameVirtualHost *:443` avant la directive `Listen 443`, et
comme expliqué dans les lignes au-dessus, remplacer

    <VirtualHost _default_:443>

par

    <VirtualHost *:443>

 dans le fichier /etc/apache2/sites-available/default-ssl.

Il faut maintenant activer les hôtes virtuels avant de redémarrer
Apache.

`# a2ensite cal `

`# a2ensite ssl-cal `

Et voilà ! Je peux maintenant accéder à mon calendrier à l'adresse
http://cal.ezvan.fr/paul/home, ou même https://cal.ezvan.fr/paul/home si
ne je veux pas que mon mot de passe passe en clair sur le réseau.

Maintenant, comment faire pour que mon Iphone qui n'utilise pas les
ports HTTP standards ne soit pas perdu ? Et bien il faut configurer
Apache pour écouter sur ces nouveaux ports !

Comment faire ? Il suffit de rajouter les directives qui vont bien dans
le fichier /etc/apache2/ports.conf : ` `

`NameVirtualHost *:8008 `

`Listen 8008 `

`NameVirtualHost *:8443 `

`Listen 8443 `

Puis dans les fichiers de configuration des hôtes virtuels précédemment
créés, il suffit de dupliquer la configuration de l'hôte virtuel en
changeant le numéro de port. Donc, rien de plus simple ! Il n'a plus
qu'à ouvrir les ports dans le firewall, redémarrer Apache et tout roule.

Maintenant, j'ai donc un calendrier et un carnet d'adresses synchronisés
dans Evolution et dans l'Iphone. N'est-ce pas beau ?

