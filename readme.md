

## Mise à jour des packages

Pour récupérer les packages utilisés par l'environnement Python :

```bash
pip freeze > requirements.txt
```

Pour installer les packages automatiquement à partir du fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

Vous pouvez également utiliser `python -m pip install -r requirements.txt` pour installer les packages.

## Copie de fichiers à distance via SCP

Pour copier depuis système local vers un système distant 

```bash
scp localfile user@host:/path/to/whereyouwant/thefile
# Par exemple, pour copier un fichier dans un sous-dossier des documents de l'utilisateur PI
scp main.py pi@192.168.1.49:~/Documents/python/encoding
```
ou pour copier depuis le système distant

```bash
scp user@host:/path/to/remotefile localfile
```


```bash
pip3 install --user virtualenv
python3 -m venv monenvironnement
```

```bash
pi@raspberrypi:~/Documents/python/encoding $ source venv/bin/activate
(venv) pi@raspberrypi:~/Documents/python/encoding $ 
```