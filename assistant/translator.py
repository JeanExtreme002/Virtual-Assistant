from googletrans import Translator
from mlconjug3 import Verbiste


class Translator(Translator):

    __pool = dict()
    __verbsList = {}


    def translate(self,text,dest="en",src="auto"):
        """
        Método para traduzir o texto de um idioma para outro.
        """

        dest = dest.lower()
        src = src.lower()
        key = "%s:%s"%(dest,src)

        # Caso o idioma de destino não exista no dicionário, ele será adicionado.
        if not key in self.__pool:
            self.__pool[key] = dict()

        # Caso já tenha sido realizado uma tradução do texto para um determinado 
        # idioma de destino, não será necessário solicitar novamente da Google.
        # Dessa forma, o retorno fica mais rápido.

        if text in self.__pool[key]:
            return self.__pool[key][text]
        
        # Obtém da Google a tradução do texto. 
        # Após isso, a tradução será adicionado ao dicionário e o resultado será retornando.
        result = super().translate(text,dest,src)
        
        self.__pool[key][text] = result
        return result


    def getVerbs(self,text,language,confidence=0.70):
        """
        Método para retornar uma lista com todos os verbos de uma frase.

        Param language: Linguagem de origem.
        Param confidence: Porcentagem mínima de confiaça que o resultado deve ter. 
        """

        verbs = []
        language = language.lower()

        if not language in self.__verbsList:
            self.__verbsList[language] = Verbiste(language)
        verbste = self.__verbsList[language]

        # Percorre cada palavra da frase.
        for w in text.split():
            
            if w.lower() in verbste.verbs: 
                verbs.append(w)
                continue

            # Obtém o resultado.
            result = self.translate(w,"en",language).extra_data
            confidence_ = result['confidence']
            synonyms = result['synonyms']

            # Se confidence_ for None, ele terá a confiança de zero porcento.
            if not confidence_:
                confidence_ = 0

            # Verifica se a confiança do resultado é maior ou igual ao parâmetro confidence.
            if confidence_ >= confidence:

                if synonyms:

                    # Procura pelo verbo.
                    for tag in synonyms:
                        if tag[0].lower() == "verb":
                            verb = tag[-1]
                            verbs.append(verb)
        return verbs
