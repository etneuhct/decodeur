

class SubstitutionMono:

    """
    Permet de procedeer a un decryptage par
    Substitution monoalphabetique
    """

    def __init__(self, texte_a_decoder, langue):
        chemin_acces_dictionnaire = "dictionnaires/{}.txt".format(langue)

        self.texte_a_decoder = texte_a_decoder

        with open(chemin_acces_dictionnaire, "rb") as fichier_dictionnaire:
            dictionnaire = fichier_dictionnaire.read().decode().upper()

        # On recupere la liste de mot de la langue d'origine
        # Et celle du texte a decode
        self.dictionnaire_langue_originale = dictionnaire.split("\r\n")
        self.dictionnaire_texte_a_decode = texte_a_decoder.split(" ")

        self.dictionnaire_texte_a_decoder_recode = self.recoder_dictionnaire()

        self.dictionnaire_langue_originale =self.supprimer_mots_inutiles()

        # On recupere l'alphabet de la langue d'origine
        # Et les lettres utilisees dans le texte code
        self.alphabet_langue_originale = list(set("".join(self.dictionnaire_langue_originale)))
        self.alphabet_texte_a_decode = list(set(list(self.texte_a_decoder.replace(" ", ""))))

        # On definit les tableaux de frequence pour chaque dictionnaire
        self.tableau_frequence_texte_a_decode = self.get_tableau_frequence(self.alphabet_texte_a_decode,
                                                                        self.dictionnaire_texte_a_decode)
        self.tableau_frequence_langue_originale = self.get_tableau_frequence(self.alphabet_langue_originale,
                                                                        self.dictionnaire_langue_originale)

        self.possibilites = self.lister_possibilites()
        self.filtrer_possibilites_incoherentes()

        self.deduction_possibilites()

    @staticmethod
    def recoder_mot(mot):
        liste_lettres = list(mot)
        result = "".join([str(liste_lettres.index(element)) for element in liste_lettres])
        return result

    def recoder_dictionnaire(self):
        result = []
        for mot in self.dictionnaire_texte_a_decode:
            result.append(self.recoder_mot(mot))
        return list(set(result))

    def supprimer_mots_inutiles(self):
        result = []
        for mot in self.dictionnaire_langue_originale:
            if self.recoder_mot(mot) in self.dictionnaire_texte_a_decoder_recode:
                result.append(mot)
        return result

    @staticmethod
    def get_tableau_frequence(alphabet, source):
        tableau_frequence = {}
        for lettre in alphabet:
            tableau_frequence[lettre] = {}
            for mot in source:
                if lettre in mot:
                    occurence = [index for index, value in enumerate(list(mot)) if value == lettre]
                    for i in occurence:
                        if i in tableau_frequence[lettre]:
                            tableau_frequence[lettre][i].append(mot)
                        else:
                            tableau_frequence[lettre][i] = [mot]
        return tableau_frequence

    def lister_possibilites(self):
        possibilities = {}
        for element in self.alphabet_texte_a_decode:
            possibilities[element] = []
            for item in self.alphabet_langue_originale:
                possibilities[element].append(item)
        return possibilities

    def filtrer_possibilites_incoherentes(self):
        for element in self.tableau_frequence_texte_a_decode:
            for item in self.tableau_frequence_langue_originale:
                for key_element in self.tableau_frequence_texte_a_decode[element]:
                    if key_element not in self.tableau_frequence_langue_originale[item].keys():
                        if item in self.possibilites[element]:
                            self.possibilites[element].remove(item)
                    else:
                        if len(self.tableau_frequence_langue_originale[item][key_element]) < \
                                len(self.tableau_frequence_texte_a_decode[element][key_element]):
                            if item in self.possibilites[element]:
                                self.possibilites[element].remove(item)

    def deduction_possibilites(self):
        for element in self.possibilites:
            if len(self.possibilites[element]) == 1:
                etat = False
                for item in self.possibilites:
                    if item != element and self.possibilites[element][0] in self.possibilites[item]:
                        self.possibilites[item].remove(self.possibilites[element][0])
                        etat = True
                if etat:
                    self.deduction_possibilites()

    def decoder(self):
        deduction = []
        for element in self.texte_a_decoder.split(" "):
            mot = []
            for item in list(element):
                if len(self.possibilites[item]) == 1:
                    mot.append(self.possibilites[item][0])
                else:
                    mot.append("?")
            mot = "".join(mot)
            deduction.append(mot)
        return " ".join(deduction)


text = "AWKTGSALLTFM HABALLOGFL KTDZSABAL ROLEKTROMTKAOL KGMOLLTL UKODALLOTN HAFAEITKTN TDZAKUGL EASRTOKAL OFEKWLMTKAOL " \
       "RTUGMTKAOTFM UWTKKGOTKA RTZGWSALLOGFL DOMIKORAMOGFL RTKTUSALLTL TEGWXOSSGFFAFM AYYAZWSTT DAKUOFALLOGFL ZAHMOLDAWV " \
       "RTKGEIALLT YSWMAOTFM TZGWOSSAFMAMTL KTMTKLTL AHHTMADTL ASWFAOM MKOLLTKAOM RKAUTOYOALLTL TFRAWZTKAOM " \
       "YOFSAFROLAOM OFLGSADTL HTOFMWKSWKTK RTHAFFTKTFM AHHKGEITKGFM HTKLOLMOGFL EGFROMOGFFOTN IBHGUALMKTL EIAZST " \
       "KOZAWRTJWOFL HKTLLAFML PALHOFAM HGKMT-GWMOSL DWTKGFL YAFTFM UASGHAFML TLJWOXTKAOTFM ITKOLLTT MAHOFAMTL AHGLMKGHITKTFM " \
       "OFRWLMKOASOLAFM OSSWLOGFFTK ZOMMAO RTEIKOLMOAFOLTKTN RGSGOKT YGSOGMTKTN XOGSAEALLOGFL HTKYGKTWLTL LHAMOASOLTKAL " \
       "KTFEIAOFAL ASEASOLTK RTUKOLAOM APGWKAM TESOHLALLTFM DAFGJWAOM OFEKODOFAM EIAFMKT KTTVADOFT ALLTKXOLLTWK EIOYYGFFTL " \
       "LTKXOLLT"

a = SubstitutionMono(text, "fr").decoder()
print(a)