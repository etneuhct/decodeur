

class Utils:

    @staticmethod
    def recoder_mot(mot):
        liste_lettres = list(mot)
        result = "".join([str(liste_lettres.index(element)) for element in liste_lettres])
        return result
