# HOW TO

Pour lancer le programme il y a 3 manières de procéder :

* Lancer `<raccourci Python 3> ./run.py <chemin trace>` (ex : `python3 ./run.py ~/Documents/trace.txt`).
* Utiliser le `Makefile` : il faut ouvrir le fichier `Makefile` et modifer la ligne `PYTHON_PATH=python` pour `PYTHON_PATH=<raccourci Python 3>` avec `<raccourci Python 3>` l'alias pour lancer Python 3, ou le chemin d'accès vers Python 3.
  * Le programme demandera alors de renseigner le chemin vers la trace.
* Lancer `<raccourci Python 3> ./run.py` (ex: `python3 ./run.py`).
  * Idem




Les 3 méthodes sont valables et arrivent au même résultat. Cependant, nous recommandons la méthode 3 pour la simplicité.

⚠️ **<u>Attention : si l'affichage semble bizarre et échoue à afficher certains caractères (�, ￼ ou autre), nous recommandons d'utiliser le « safe mode ».</u>** ⚠️ Cela est dû à une incompatibilité de la police de votre terminal.
