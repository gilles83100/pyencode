# Conversion de vidéo

Pour système sous Windows, Mac OS, Raspbian (raspberry PI).

Packages :

    progressbar2

Commandes

* Conversion simple avec codecs par défaut

```
python3 main.py -i source -o destination
```

* Conversion simple avec définition du codec de compression vidéo

```
python3 main.py -i source -o destination -codecvideo libx264
```