Title: Fedora 21, Backlight et Samsung Ultra NP740U3E
Date: 2014-12-20 01:22
Author: Paul Ezvan
Slug: fedora-21-backlight-et-samsung-ultra-np740u3e

<div
class="field field-name-body field-type-text-with-summary field-label-hidden">

<div class="field-items">

<div class="field-item even">

Pour faire fonctionner le réglage du rétro-éclairage (backlight) du
Samsung Series 7 Ultra NP740U3E sous Fedora 21, voici l'astuce.

</p>
Ajouter

</p>
    video.use_native_backlight=0

à la ligne GRUB\_CMDLINE\_LINUX dans /etc/default/grub.

</p>
Régénerer le fichier de configuration Grub (dans le cas d'un démarrage
EFI):

</p>
    sudo grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg

Attention ! Ne pas utiliser Intel-backlight dans la configuration Xorg !
Cela ne fonctionne pas avec ce portable.

</p>

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

[Libre](https://www.ezvan.fr/taxonomy/term/48)

</div>

</div>

</div>

</p>

