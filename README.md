# chess
**Projet python avancé de Samuel Bourdeau, Gabin Sagot, Yanis Hadj Mohand**

Pour jouer au jeu d'échecs  :

Installer les librairies présentes dans le fichier requirement.txt en faisant :
    pip install -r requirements.txt

Exécuter le fichier main.py, et jouer !
Pour déplacer une pièce, cliquer sur la pièce, puis cliquer sur sa position souhaitée (ces dernières sont alors grisées).

**Etat des lieux du projet**
Voici une liste de ce qui fonctionne :
- Les déplacements licites des pièces ont tous été implémentés
- Le roque fonctionne (et est impossible une fois que le roi a bougé)
- La promotion de pions fonctionne : une fois le pion arrivée en bout de rangée, taper dans le terminal la première lettre de la pièce vers laquelle on souhaite avoir une promotion

Voici une liste de ce que nous avons tenté d'implémenter, mais avons échoué à faire malgré de nombreuses tentatives : 

- Le système de victoire par mat ne fonctionne pas, malgré les fonctions implémentées en ce but
- Nous souhaitions que la case du roi se colore en orange en cas d'échec, en rouge en cas de mat. Cela n'a pas fonctionné. 
- La prise en passant n'a pas été implémentée. 



