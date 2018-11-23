Title: Linux et la seconde intercalaire
Date: 2012-07-03 08:49
Author: Paul
Tags: Linux, Libre
Slug: linux-et-la-seconde-intercalaire

Si vous avez observé des dysfonctionnements sur vos serveurs Linux le
premier juillet, cela vient probablement d'un bogue du noyau Linux, qui
a eu quelques problèmes pour gérer [la seconde
intercalaire](https://fr.wikipedia.org/wiki/Seconde_intercalaire) du 30
juin.

La seconde intercalaire est une seconde ajoutée pour resynchroniser
l'heure UTC avec l'heure réelle. La dernière minute du 30 juin a donc
duré 61 secondes, ce qui peut provoquer certains remous lorsque cette
situation est mal gérée par le logiciel.

À priori, le noyau Linux, Java, MySQL et d'autres sont impactés. Parmi
les "gros" du web impactés, on compte Reddit, Linkedin, Foursquare,
Mozilla...

[Plus d'info sur
Serverfault](http://serverfault.com/questions/403732/anyone-else-experiencing-high-rates-of-linux-server-crashes-during-a-leap-second)

[Un exemple de problème chez
Mozilla](https://blog.mozilla.org/it/2012/06/30/mysql-and-the-leap-second-high-cpu-and-the-fix/)

[De même chez
Linuxfr](https://linuxfr.org/users/nono/journaux/leap-second)

