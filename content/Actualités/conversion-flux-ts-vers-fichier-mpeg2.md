Title: Conversion flux TS vers fichier MPEG2
Date: 2007-04-22 09:54
Author: Dominique
Tags: Logiciels de Papa, DVBT2MPG
Slug: conversion-flux-ts-vers-fichier-mpeg2
Lang: fr

La mise au point de l'outil DVBT2MPG pour l'extraction des
enregistrements audio/vidéo du PVR SAGEM m'a fait découvrir le problème
de désynchronisation entre le son et l'image propre à la TNT. En effet,
les transmissions herziennes ne sont pas parfaites et l'intégralité des
données ne parvient pas au récepteur et enregistreur numérique.  

Les émissions étant diffusées au format TS (*Transport Stream* ou flux
de transport), l'enregistrement est généralement fait dans ce format.
Pour pouvoir exploiter ces vidéos sur un PC, il est préférable de
disposer de fichiers au format PS (*Program Stream* ou flux programme).
L'idée est donc de refaire le synchronisation du son et de l'image lors
de la conversion de format.  

Afin de permettre l’utilisation de ce convertisseur pour d'autres PVR ou
d’autres sources comme des cartes tuner TNT, j’ai crée l’outil
[TS2MPG]({filename}/pages/logiciels-papa.md) qui ne contient que le
convertisseur. Il permet d’extraire un fichier MPEG2 à partir d’un flux
TS disponible sous forme de fichier avec la possibilité de sélectionner
la piste audio.


