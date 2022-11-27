# Wirewhale



Ce projet cherche à reproduire une version très minimale du contenu de l'analyse mode *Flow chart* proposée par Wireshark. L'analyse n'est pas en temps réel : il faut fournir un fichier trace contenant les octets des communications.

L'outil est capable d'analyser les protocoles suivants :

* Ethernet
* IP (version 4)
* TCP
* HTTP

⚠️Tout protocole autre provoquera un **refus d'analyse de la trame en question** (HTTP est optionnel ; l'analyseur peut se passer de la présence de ce protocole et s'arrêter au segment TCP).

### Entrée

Le fichier trace doit **absolument** être formatté selon la manière de faire de Wireshark. Pour exporter un fichier au format correct, il faut :

* Lancer Wireshark et démarrer l'analyse en temps réeel/ouvrir le fichier au format PCAPNG
* File → Export Packets Dissections → As Plain Text
* ⚠️ **Décocher « Packet summary line », « Include column headings » et « Packet details »**
* ⚠️ **Cocher « Packet bytes »**
* Sauvegarder

Exemple de trame valide à l'entrée : 

```
0000  f0 18 98 59 ae 32 0c 8d db 1a 1e 88 08 00 45 00   ...Y.2........E.
0010  00 34 e7 8e 40 00 2d 06 cc 41 80 77 f5 0c c0 a8   .4..@.-..A.w....
0020  63 c7 00 50 ed 6b a3 f0 18 33 c0 8a 8f 98 80 11   c..P.k...3......
0030  00 eb 64 02 00 00 01 01 08 0a 94 5c 05 8d 43 88   ..d........\..C.
0040  a0 66                                             .f
```

### Code

La structure du code est relativement simple :

* <u>Le parser</u> est une classe. Elle s'initie avec le chemin vers le fichier trace, qui est lu et décodé pour être analysé par la suite. En voici un prototype :

  ```py
  class Parser:
      def __init__(self, path): ...
      
      def clean_data(self): ...
      def parse(self, frames): ...
      
      def analyze_frame(self, frame): ...
      def scan_ipv4_headers(self, frame): ...
      def scan_tcp_headers(self, frame): ...
      def scan_http_headers(self, frame): ...
  ```

  

* Les données brutes sont nettoyées et transformées en un liste de strings, qui correspondent chacune à une trame, dans `clean_data` puis dans `parser`.

* Chaque couche de la trame dispose d'une méthode de `Parser` dédiée pour analyser son contenu.

* Ces dernières méthodes s'appellent les unes les autres :

  * La méthode `analyze_frame` récupère les informations de la trame Ethernet, constitue un dictionnaire et le joint au résultat de l'appel de la fonction suivante ;
  * La méthode `scan_ipv4_headers` récupère les informations du paquet IP, constitue un dictionnaire et le joint au résultat de l'appel de la fonction suivante ;
  * La méthode `scan_tcp_headers` récupère les informations du segment TCP, constitue un dictionnaire et le joint au résultat de l'appel de la fonction suivante ;
  * La méthode `scan_http_header` récupère les données HTTP (si elles existent), constitue un dictionnaire de ses attributs et le renvoie.

On a donc `analyze_frame ∪ (scan_ipv4_headers ∪ (scan_tcp_headers ∪ scan_http_header))`.

Une petite classe et différentes fonctions utilitaires existent dans le fichier `utils` et servent à gérer l'affichage ou simplifier le code de `Parser`. Elles ne seront pas détaillées ici.

