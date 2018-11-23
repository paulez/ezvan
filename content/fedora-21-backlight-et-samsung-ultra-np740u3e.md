Title: Fedora 21, Backlight et Samsung Ultra NP740U3E
Date: 2014-12-20 01:22
Author: Paul Ezvan
Tags: Libre
Slug: fedora-21-backlight-et-samsung-ultra-np740u3e

Pour faire fonctionner le réglage du rétro-éclairage (backlight) du
Samsung Series 7 Ultra NP740U3E sous Fedora 21, voici l'astuce.

Ajouter

    video.use_native_backlight=0

à la ligne GRUB\_CMDLINE\_LINUX dans /etc/default/grub.

Régénerer le fichier de configuration Grub (dans le cas d'un démarrage
EFI):

    sudo grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg

Attention ! Ne pas utiliser Intel-backlight dans la configuration Xorg !
Cela ne fonctionne pas avec ce portable.

