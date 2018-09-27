from utils import Utils


class GestionnaireMot:

    def __init__(self, dictionnaire_langue_originale_classe, dictionnaire_langue_codee):

        self.dictionnaire_correspondance_mot = {
            mot_code: dictionnaire_langue_originale_classe[Utils.recoder_mot(mot_code)]
                for mot_code in dictionnaire_langue_codee}

    def verification_de_mot_trouve(self):
        for mot_code in self.dictionnaire_correspondance_mot:
            if len(self.dictionnaire_correspondance_mot[mot_code]) == 1 and \
                    isinstance(self.dictionnaire_correspondance_mot[mot_code], list):
                self.dictionnaire_correspondance_mot[mot_code] = self.dictionnaire_correspondance_mot[mot_code][0]
                #return self.actualiser_dictionnaire_correspondance_mot()

    def suppression_de_mot_trouve(self):
        liste_mots_uniques = set([element for element in self.dictionnaire_correspondance_mot.values() if isinstance(element, str)])
        for mot_code in self.dictionnaire_correspondance_mot:
            if isinstance(self.dictionnaire_correspondance_mot[mot_code], list) and \
                            len(self.dictionnaire_correspondance_mot[mot_code]) > 1:
                nouvelle_liste = list(set(self.dictionnaire_correspondance_mot[mot_code]) - liste_mots_uniques)
                if len(nouvelle_liste) == 1:
                    self.dictionnaire_correspondance_mot[mot_code] = nouvelle_liste[0]
                    return self.actualiser_dictionnaire_correspondance_mot()
                else:
                    self.dictionnaire_correspondance_mot[mot_code] = nouvelle_liste

    def suppression_par_n_mot_necessaire(self):

        # A ameliorer
        liste_possibilites_non_trouvees = [sorted(element) for element in self.dictionnaire_correspondance_mot.values() if
                                           isinstance(element, list)]
        possibilites_necessaire = []
        for element in liste_possibilites_non_trouvees:
            if element not in possibilites_necessaire and \
                            liste_possibilites_non_trouvees.count(element) == len(element):
                possibilites_necessaire.append(element)

        for possibilites in possibilites_necessaire:
            for mot in possibilites:
                for mot_code in self.dictionnaire_correspondance_mot:
                    if sorted(self.dictionnaire_correspondance_mot[mot_code]) != sorted(possibilites) \
                            and mot in self.dictionnaire_correspondance_mot[mot_code]:
                        self.dictionnaire_correspondance_mot[mot_code].remove(mot)
                        return self.actualiser_dictionnaire_correspondance_mot()

    def suppression_par_mot_absent_dictionnaire_lettre_lettre_trouvee(self, dictionnaire_lettre):
        lettre_codee_trouvee = {cle: dictionnaire_lettre[cle] for cle in dictionnaire_lettre if isinstance(dictionnaire_lettre[cle], str)}
        for lettre in lettre_codee_trouvee:
            for mot_code in self.dictionnaire_correspondance_mot:
                if lettre in mot_code and isinstance(self.dictionnaire_correspondance_mot[mot_code], list):
                    position = list(mot_code).index(lettre)
                    nouvelle_liste = [mot for mot in self.dictionnaire_correspondance_mot[mot_code]
                                      if mot[position] == lettre_codee_trouvee[lettre]]

                    if len(nouvelle_liste) == 1:
                        self.dictionnaire_correspondance_mot[mot_code] = nouvelle_liste[0]
                        return self.actualiser_dictionnaire_correspondance_mot(dictionnaire_lettre)
                    else:
                        self.dictionnaire_correspondance_mot[mot_code] = nouvelle_liste

    def suppression_par_mot_absent_dictionnaire_lettre_position_lettre_trouvee(self, dictionnaire_lettre):
        lettre_codee_position_trouvee = {cle: dictionnaire_lettre[cle] for cle in dictionnaire_lettre if
                                isinstance(dictionnaire_lettre[cle], dict)}

        for lettre in lettre_codee_position_trouvee:
            for mot_code in self.dictionnaire_correspondance_mot:
                if lettre in mot_code and isinstance(self.dictionnaire_correspondance_mot[mot_code], list):
                    position_list = [i for i in range(len(mot_code)) if mot_code[i] == lettre]
                    for position in position_list:
                        nouvelle_liste = [mot for mot in self.dictionnaire_correspondance_mot[mot_code]
                                          if mot[position] in lettre_codee_position_trouvee[lettre][position]]

                        if len(nouvelle_liste) == 1:
                            self.dictionnaire_correspondance_mot[mot_code] = nouvelle_liste[0]
                            return self.actualiser_dictionnaire_correspondance_mot(dictionnaire_lettre)
                        else:
                            self.dictionnaire_correspondance_mot[mot_code] = nouvelle_liste

    def actualiser_dictionnaire_correspondance_mot(self, dictionnaire_lettre=None):

        self.verification_de_mot_trouve()
        self.suppression_de_mot_trouve()
        self.suppression_par_n_mot_necessaire()

        if dictionnaire_lettre:
            self.suppression_par_mot_absent_dictionnaire_lettre_lettre_trouvee(dictionnaire_lettre)
            self.suppression_par_mot_absent_dictionnaire_lettre_position_lettre_trouvee(dictionnaire_lettre)