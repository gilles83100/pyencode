# Conversion de vidéo

Pour système sous Windows, MacOS, Raspbian (raspberry PI).

Packages :

    progressbar2

[ffmpeg.exe](https://www.ffmpeg.org) à installer à la racine du projet

Commandes :

* Conversion simple avec codecs par défaut

```
python3 main.py -i source -o destination
```

* Conversion simple avec définition du codec de compression vidéo

```
python3 main.py -i source -o destination -codecvideo libx264
```
