from utils import Utils
from gestionnaire_mot import GestionnaireMot
from gestionnaire_lettre import GestionnaireLettre


class SubstitutionMono:

    def __init__(self, text, langue):

        self.text = text.upper()
        chemin_acces_dictionnaire = "dictionnaires/{}.txt".format(langue)

        with open(chemin_acces_dictionnaire, "rb") as fichier_dictionnaire:
            self.dictionnaire_langue_originale = fichier_dictionnaire.read().decode().upper()

        self.alphabet_langue_originale = list(set(self.dictionnaire_langue_originale.replace("\r\n", "")))

        self.dictionnaire_langue_originale = self.dictionnaire_langue_originale.split("\r\n")
        self.dictionnaire_langue_codee = list(set(self.text.split(" ")))

        self.alphabet_langue_codee = list(set(self.text))
        self.alphabet_langue_codee.remove(" ")


    def classer_mot_dictionnaire_langue_original(self):
        dictionnaire_langue_originale_classe = {}
        for mot in self.dictionnaire_langue_originale:
            cle = Utils.recoder_mot(mot)
            if cle not in dictionnaire_langue_originale_classe:
                dictionnaire_langue_originale_classe[cle] = []
            dictionnaire_langue_originale_classe[cle].append(mot)
        return dictionnaire_langue_originale_classe

    def identification_lettres(self):

        gestionnaire_de_mot = GestionnaireMot(
            self.classer_mot_dictionnaire_langue_original(),
            self.dictionnaire_langue_codee)

        gestionnaire_de_mot.actualiser_dictionnaire_correspondance_mot()

        while 1 :
            dictionnaire_correspondance_mot = gestionnaire_de_mot.dictionnaire_correspondance_mot
            dictionnaire_correspondance_mot_t_0 = dict(dictionnaire_correspondance_mot)

            gestionnaire_de_lettre = GestionnaireLettre(dictionnaire_correspondance_mot)
            gestionnaire_de_lettre.actualiser_dictionnaire_lettre(dictionnaire_correspondance_mot)

            dictionnaire_correspondance_lettre = gestionnaire_de_lettre.dictionnaire_correspondance_lettre

            gestionnaire_de_mot.actualiser_dictionnaire_correspondance_mot(dictionnaire_correspondance_lettre)

            arreter = dictionnaire_correspondance_mot_t_0 == dict(dictionnaire_correspondance_mot)

            if arreter: return dictionnaire_correspondance_lettre

    def decoder(self):
        dictionnaire_correspondance_lettre = self.identification_lettres()
        lettre_trouvee = {}
        for lettre in dictionnaire_correspondance_lettre:
            if isinstance(dictionnaire_correspondance_lettre[lettre], str):
                lettre_trouvee[lettre] = dictionnaire_correspondance_lettre[lettre]

        resultat = []
        for element in list(self.text):
            if element in lettre_trouvee.keys():
                resultat.append(lettre_trouvee[element])
            elif element == " ":
                resultat.append(" ")
            else:
                resultat.append("?")
        result = "".join(resultat)

        print(list(result.replace(" ", "")).count("?")/len(list(result.replace(" ", ""))))
        print(result)

text = "EIAEWF HTWM LT HKTXASGOK RT MGWL STL RKGOML TM RT MGWMTL STL SOZTKMTL HKGESADTL RAFL SA HKTLTFMT RTESAKAMOGF LAFL ROLMOFEMOGF"

SubstitutionMono(text, "fr").decoder()