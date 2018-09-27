Ce programme permet de décrypter un texte coder par substitution mono alphabétique.

Note :
* On part du principe que la version originale des mots cryptés existe dans un fichier.
* Les signes de ponctuation ne sont pas gérés. 
* Les lettres accentuées ne sont pas considérées comme des lettres non accentuées.

Logique :

On commence par créer un **dictionnaire de mot** qui permet de matcher 
les mots codés aux mots qui pourraient en être les originaux. 
Cela est possible en identifiant l'agencement des lettres de chaque mot. 
Par exemple, le mot "AZEREPI" aurait pour schémas "0.1.2.3.2.5.6". 
On associerait donc tous les mots dont le schémas serait "0.1.2.3.2.5.6" 
aux mots originaux possibles de "AZEREPI".

On procède ensuite recursivement à plusieurs étapes.

A. Dans le dictionnaire de mots
1. Eliminer de la liste de possibilites des mots codés les mots originaux qui ont deja été trouvés
2. Eliminer de la liste de possibilites des mots codés les mots originaux qui sont nécessairement 
les originaux de mots identifiés
> Dans le cas:
dictionnaire_de_mots = {"0": ["A", "B", "C"], "1": ["A", "B", "C"], "2": ["A", "B", "C"], "3": ["D", "A]}
les termes "A", "B" et "C" sont nécessairement les originaux des termes "0", "1" et "2". Il faut donc éliminer
"A" des possibilites de "3".

B. Dans le dictionnaire de lettre
> Determiner un dictionnaire de lettre qui fait correspondre a chaque lettre cryptée les originaux possibles
en fonction de la position dans le mot.
4. Eliminer de la liste des possibilites de chaque lettre cryptee, les lettres qui n'appartiennent pas à 
la liste obtenue par l'intersection entre les listes de possibilites par position de la lettre cryptée concernée
> Dans le cas: 
dictionnaire_de_lettre = {"A": {"position_0": ["B", "D", "F], "position_2": ["B", "X", "R]}}
seul le terme "B" sera conservé, car présent dans toutes les listes.
5. Eliminer de la liste de possibilites des lettres cryptées, les lettres qui ont deja ete trouvee
6. Eliminer de la liste de possibilites des lettres cryptées, les lettres qui sont nécessairement 
les originaux de lettres identifiées
> Meme logique que dans le cadre du dictionnaire de mot

C. Dans le dictionnaire de mot
7. Eliminer de la liste de mots possibles de chaque mot crypté les mots dont le positionnement des lettres
ne correspond pas avec le dictionnaire de lettre
> Dans le cas:
dictionnaire_de_lettre = {"Q": {"position_0": ["B", "W"]}}
dictionnaire_de_mot = {"QWERTY" : ["XAVIER", "BRAISE"]]
Le terme "XAVIER" sera exclu du dictionnaire car à la position 0,
la lettre "X" n'est pas acceptée comme l'équivalent de "Q"

***On recommence jusqu'à ce que la méthode ne provoque plus de changement au sein du dictionnaire de mots.***