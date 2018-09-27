

class GestionnaireLettre:

    def __init__(self, dictionnaire_correspondance_mot):

        self.dictionnaire_correspondance_lettre = {}

        for mot_code in dictionnaire_correspondance_mot:
            list_lettre_code = list(mot_code)

            if isinstance(dictionnaire_correspondance_mot[mot_code], str) :
                for lettre_code in set(list_lettre_code):
                    index_lettre_code = list_lettre_code.index(lettre_code)
                    self.dictionnaire_correspondance_lettre[lettre_code] = dictionnaire_correspondance_mot[mot_code][
                        index_lettre_code]

            elif isinstance(dictionnaire_correspondance_mot[mot_code], list) :

                for lettre_code in set(list_lettre_code):

                    positions_lettre_code = [i for i in range(len(list_lettre_code))
                                        if list_lettre_code[i] == lettre_code]

                    if lettre_code not in self.dictionnaire_correspondance_lettre:
                        self.dictionnaire_correspondance_lettre[lettre_code] = {}

                        for position in positions_lettre_code:
                            self.dictionnaire_correspondance_lettre[lettre_code][position] = list(set([
                                mot[position] for mot in dictionnaire_correspondance_mot[mot_code]]))

                    elif isinstance(self.dictionnaire_correspondance_lettre[lettre_code], dict):

                        for position in positions_lettre_code:

                            if position not in self.dictionnaire_correspondance_lettre[lettre_code].keys():
                                self.dictionnaire_correspondance_lettre[lettre_code][position] = list(set([
                                    mot[position] for mot in dictionnaire_correspondance_mot[mot_code]]))

                            else:
                                self.dictionnaire_correspondance_lettre[lettre_code][position] = list(
                                    set([mot[position] for mot in dictionnaire_correspondance_mot[mot_code]])
                                                            &
                                    set(self.dictionnaire_correspondance_lettre[lettre_code][position]))

    def suppression_de_lettre_par_intersection_de_position(self):
        for lettre in self.dictionnaire_correspondance_lettre:
            if isinstance(self.dictionnaire_correspondance_lettre[lettre], dict) and len(self.dictionnaire_correspondance_lettre[lettre]) > 1:
                positions = sorted(list(self.dictionnaire_correspondance_lettre[lettre].keys()))
                nouvelle_liste = set(self.dictionnaire_correspondance_lettre[lettre][positions[0]])
                for position_possible in positions[1:]:
                    nouvelle_liste = nouvelle_liste & set(self.dictionnaire_correspondance_lettre[lettre][position_possible])
                nouvelle_liste = list(nouvelle_liste)

                for position_possible in positions:
                    if len(nouvelle_liste) == 1:
                        self.dictionnaire_correspondance_lettre[lettre] = nouvelle_liste[0]
                    else:
                        self.dictionnaire_correspondance_lettre[lettre][position_possible] = nouvelle_liste

    def suppression_de_lettre_par_lettre_trouve(self):
        lettres_trouvees = [self.dictionnaire_correspondance_lettre[lettre]
                          for lettre in self.dictionnaire_correspondance_lettre
                          if isinstance(self.dictionnaire_correspondance_lettre[lettre], str)]
        for lettre in self.dictionnaire_correspondance_lettre:


            if isinstance(self.dictionnaire_correspondance_lettre[lettre], dict):
                for position in self.dictionnaire_correspondance_lettre[lettre]:
                    nouvelle_liste = list(
                                    set(self.dictionnaire_correspondance_lettre[lettre][position])
                                                -
                                    set(lettres_trouvees))

                    if len(nouvelle_liste) == 1:
                        self.dictionnaire_correspondance_lettre[lettre] = nouvelle_liste[0]
                        return self.actualiser_dictionnaire_lettre()

                    else:
                        self.dictionnaire_correspondance_lettre[lettre][position] = nouvelle_liste

    def suppression_de_lettre_par_frequence_aberrante(self):

        return

    def actualiser_dictionnaire_lettre(self, nouveau_dictionnaire_correspondance_mot=None):

        self.suppression_de_lettre_par_intersection_de_position()
        self.suppression_de_lettre_par_lettre_trouve()
        self.suppression_de_lettre_par_frequence_aberrante()
