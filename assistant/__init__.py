from assistant.commands import AssistantCommands
from assistant.gui.itemList import ItemList
from assistant.gui.messageBox import MessageBox
from assistant.sounds import Sounds
from assistant.translator import Translator
from speech_recognition import Microphone,Recognizer
from threading import Thread
import time 
import json
import keyboard
import os


class Assistant(object):

    __defaultCommands = {
        "open":1,
        "search":2,
        "go to":3,
        "calculate":4,
        "add path":5,
        "add directory":5,
        "remove path":6,
        "remove directory":6,
        "command list":7,
        "minimize":8,
        "maximize":9,
        "close":10,
        "add command":11,
        "edit command":12,
        }
    
    __defaultCommands_PT_BR = {
        "abrir":__defaultCommands["open"],
        "pesquisar":__defaultCommands["search"],
        "procurar":__defaultCommands["search"],
        "ir para":__defaultCommands["go to"],
        "calcular":__defaultCommands["calculate"],
        "adicionar caminho":__defaultCommands["add path"],
        "adicionar diretório":__defaultCommands["add directory"],
        "remover caminho":__defaultCommands["remove path"],
        "remover diretório":__defaultCommands["remove directory"],
        "lista de comandos":__defaultCommands["command list"],
        "minimizar":__defaultCommands["minimize"],
        "maximizar":__defaultCommands["maximize"],
        "fechar":__defaultCommands["close"],
        "adicionar comando":__defaultCommands["add command"],
        "editar comando":__defaultCommands["edit command"]
        }

    __defaultLanguage = "en-us"

    __info = [
        "Open:Run a program or open a file or folder.",
        "Search:Opens the browser with a search.",
        "Go to:Opens the browser directly to a site.",
        "Calculate:Calculates a simple arithmetic expression.",
        "Add path:Adds a directory to locate programs, files, and folders.",
        "Remove path:Removes a directory added by the user.",
        "Command list:Opens a list of all voice commands.",
        "Minimize:This minimizes an active window or a window with a title you specify.",
        "Maximize:This maximizes a window with a title you specify.",
        "Close:This closes an active window or a window with a title you specify.",
        "Add command:Opens a window for defining a command and associating a program with it.",
        "Edit command:Opens a window for editing the information of a command."
    ]
    
    __info_PT_BR = [
        "Abrir:Executa um programa ou abre um arquivo ou pasta.",
        "Pesquisar:Abre o navegador com uma busca.",
        "Vá para:Abre o navegador diretamente em um site.",
        "Calcular:Calcula uma expressão aritmética simples.",
        "Adicionar caminho:Adiciona um diretório para o assistente localizar arquivos e pastas.",
        "Remover caminho:Remove um diretório adicionado pelo usuário.",
        "Lista de comandos:Abre uma lista com todos os comandos de voz.",
        "Minimizar:Minimiza uma janela ativa ou uma janela com um título específico.",
        "Maximizar:Maximiza uma janela com um título específico.",
        "Fechar:Fecha uma janela ativa ou uma janela com um título específico.",
        "Adicionar comando:Abre uma janela para definir um comando e um programa associado a ele.",
        "Editar comando:Abre uma janela para editar as informações de um comando."
    ]

    __settings = {
        "Assistant":{
            "Language":"EN-US",
            "Name":"Jarvis",
        },
        "System":{
            "Paths":[],
            "Press to speak":"left windows + s",
            "Sounds":True,
            "ShowInput":True
        }
    }

    __userCommands = {}

    __settingsFile = "settings.json"
    __commandsFile = "commands.json"

    __help = False


    def __init__(self,messageBox,settingsPath,icon=None):
        """
        O parâmetro "messageBox" deve ser um objeto de MessageBox ou de uma subclasse dela.

        O parâmetro "settingsPath" deve ser um diretório para 
        carregar e salvar as configurações do assistente.
        """

        # Verifica se messageBox é um objeto que vem de MessageBox ou sua subclasse.
        if not issubclass(type(messageBox),MessageBox): 
            raise TypeError("a MessageBox object is required (got {})".format(type(messageBox)))
        self.__messageBox = messageBox 
        self.__icon = icon 

        # Carrega as configurações do assistente.
        self.__settingsFile = os.path.join(settingsPath,self.__settingsFile)
        self.__commandsFile = os.path.join(settingsPath,self.__commandsFile)
        self.loadSettings(self.__settingsFile)
        self.loadUserCommands(self.__commandsFile)

        # Salva as configurações do assistente. 
        # Isso faz com que as informações do arquivo fiquem atualizadas caso alguma informação esteja faltando.
        self.saveSettings(self.__settingsFile)

        # Inicializa um objeto para reconhecimento de voz e tradução de texto.
        self.__recognizer = Recognizer()
        self.__translator = Translator()

        # Inicializa objeto para gerar sons.
        self.__sounds = Sounds()

        # Cria objeto da classe AssistantCommands para realizar as ações do assistente.
        self.__assistantCommands = AssistantCommands(self,self.__settings,self.__userCommands)

        # Define o idioma do assistente.
        language = self.__settings["Assistant"]["Language"]
        self.changeLanguage(language)


    def changeLanguage(self,language):
        """
        Método para trocar o idioma do assistente.
        """

        if language.lower() == "pt-br":
            self.__settings["Assistant"]["Language"] = "PT-BR"
            self.__commands = self.__defaultCommands_PT_BR
        else:
            self.__settings["Assistant"]["Language"] = "EN-US"
            self.__commands = self.__defaultCommands


    def getAssistantCommands(self):
        """
        Método para retornar uma instância de AssistantCommands.
        """
        return self.__assistantCommands


    @staticmethod
    def getCommandsFile():
        """
        Método para retornar o nome do arquivo que guarda os comandos adicionados pelo usuário.
        """
        return Assistant.__commandsFile


    @staticmethod
    def getDefaultSettings():
        """
        Retorna as configurações padrão do assistente.
        """
        return Assistant.__settings

    
    def getInfo(self):
        """
        Método para retornar as informações de todos os comandos do assistente.
        """

        # Obtém o idioma atual do assistente.
        language = self.getLanguage().lower()

        # Obtém as informações no idioma atual.
        if language == "pt-br":
            default_info = self.__info_PT_BR.copy()
        else:
            default_info = self.__info.copy()
        info = []

        # Adiciona um espaço no texto.
        for command in default_info:
            info.append(" "+command)

        # Adiciona à lista os comandos criados pelo usuário.
        for command in self.__userCommands.keys():
            info.append(
                " "+self.__userCommands[command]["Command"].capitalize()+":"+
                self.__userCommands[command]["Description"].capitalize()
                )
        return info


    def getLanguage(self):
        """
        Retorna o idioma atual do assistente.
        """
        return self.__settings["Assistant"]["Language"]


    @staticmethod
    def getSettingsFile():
        """
        Método para retornar o nome do arquivo de configurações do assistente.
        """
        return Assistant.__settingsFile


    def getTranslator(self):
        """
        Método para retornar uma instância de Translator.
        """
        return self.__translator


    def getStatus(self):
        """
        Informa se foi solicitado ou não a parada do método run().
        """
        return self.__stop


    def help(self):
        """
        Método para abrir uma lista com todos os comandos do assistente.
        """
        self.__help = True


    def __helpList(self,info,sep=":"):
        """
        Método para abrir lista de ajuda.
        """

        # Separa os títulos e as descrições.
        commands = []
        for item in info:
            commands.append(item.split(sep,maxsplit=1))
        commands.sort(reverse=True)

        # Ajusta o tamanho da lista.
        height = len(commands) if len(commands) < 10 else 10

        itemList = ItemList(
            "Assistant Commands",
            height=height,
            icon=self.__icon
            )
        itemList.run(commands,self.getStatus)
        self.__help = False



    def isRunning(self):
        """
        Informa se o método run() está em execução ou não.
        """
        return self.__running


    def loadSettings(self,settingsFile):
        """
        Método para carregar as configurações do assistente.
        """

        # Cria um arquivo com as configurações padrão caso o mesmo não exista.
        if not os.path.exists(settingsFile):
            self.saveSettings(settingsFile)
            return self.__settings

        # Carrega as configurações do arquivo.
        with open(settingsFile) as file:
            settings = json.loads(file.read())

            if "Assistant" in settings:
                self.__settings["Assistant"].update(settings["Assistant"])
            if "System" in settings:
                self.__settings["System"].update(settings["System"])

        return self.__settings
        

    def loadUserCommands(self,commandsFile):
        """
        Método para carregar os comandos adicionados pelo usuário.
        """

        # Cria um arquivo para que os comandos criados pelo usuário possam ser salvos.
        if not os.path.exists(commandsFile):
            self.saveUserCommands(commandsFile)
            return self.__userCommands

        # Carrega os comandos do arquivo.
        with open(commandsFile) as file:
            self.__userCommands = json.loads(file.read())
        return self.__userCommands


    def __press_to_speak(self):
        """
        Espera até que o usuário aperte uma determinada tecla para falar com o assistente.
        """

        # Obtém a tecla que o usuário deve pressionar para falar com o assistente.
        press_to_speak = self.__settings["System"]["Press to speak"]

        while True:
            keyboard.wait(press_to_speak)
            if self.__stop: break
            if not self.__listening:
                self.__speak = True


    def run(self):
        """
        Método para iniciar o assistente.
        """

        self.__stop = False
        self.__running = True
        self.__speak = False
        self.__listening = False

        # Obtém a tecla que o usuário deve pressionar para falar com o assistente.
        press_to_speak = self.__settings["System"]["Press to speak"]

        # Obtém a opção de som habilitado ou não.
        sounds = self.__settings["System"]["Sounds"]

        # Obtém o idioma e o nome do assistente.
        language = self.getLanguage()
        name = self.__settings["Assistant"]["Name"]

        # Informa o que o usuário deve fazer para chamar o assistente.
        if press_to_speak:

            # Inicializa uma thread para esperar até que o usuário aperte uma determinada tecla.
            Thread(target=self.__press_to_speak).start()
            text , substring = 'Press "{}" to speak.' , press_to_speak.replace("+"," + ")
        else:
            text , substring = "Speak my name to talk to me." , ""

        self.speak(
            name,
            text,
            language.split("-")[0],
            substrings = [substring,],
            wait = True,
            sound=sounds
            )

        # Ouve o usuário enquanto não for pedido para o método run() parar.
        while not self.__stop:
            
            # Informa que o assistente não está ouvindo.
            self.__listening = False

            if self.__stop: break

            if self.__help:
                self.__helpList(self.getInfo())
                self.__speak = False

            # Aguarda um tempo de milisegundos para que o programa não consuma muito processamento.
            time.sleep(0.1)

            # Verifica se o usuário apertou o botão ou não para falar.
            if press_to_speak and not self.__speak: 
                continue

            elif press_to_speak:
                 self.__speak = False
                 self.__listening = True

            # Inicializa o microfone para ouvir o aúdio.
            with Microphone() as microphone:

                # Obtém as configurações do assistente.
                language = self.getLanguage()
                name = self.__settings["Assistant"]["Name"]

                # Obtém as configurações do sistema.
                paths = self.__settings["System"]["Paths"]
                showInput = self.__settings["System"]["ShowInput"]
                sounds = self.__settings["System"]["Sounds"]
                showInput = self.__settings["System"]["ShowInput"]

                # Ajusta o Recognizer para o som do ambiente atual.
                self.__recognizer.adjust_for_ambient_noise(microphone)

                # Reproduz um som, informando que o assistente está ouvindo o usuário.
                if sounds: self.__sounds.play_sound(self.__sounds.listening_fn)

                # Informa que o assistente está ouvindo.
                self.speak(
                    name,"I'm listening...",language.split("-")[0],
                    duration=2,wait=False,sound=None
                    )

                # Tenta ouvir o usuário e realizar o reconhecimento de voz.
                try:

                    # Obtém o aúdio do microfone.
                    audio = self.__recognizer.listen(microphone)

                    if self.__stop: break

                    # Realiza o reconhecimento de voz.
                    text = self.__recognizer.recognize_google(audio,language=language)

                except Exception as e: 

                    if press_to_speak:

                        # Informa que houve algum problema ao realizar o reconhecimento de voz.
                        self.speak(
                            name,"I'm sorry, but I can't understand what you said.",
                            language.split("-")[0],wait=True,sound=sounds
                            )
                    continue

                # Obtém o idioma para realizar a tradução do assistente para o usuário.
                language = language.split("-")[0]

                # Mostra o que o reconhecimento entendeu do que foi dito pelo usuário.
                if showInput:
                    title = self.__translator.translate(
                        "You said:",
                        language,
                        self.__defaultLanguage.split("-")[0]
                        ).text
                    self.speak(title,'"%s"'%text,duration=2,wait=True)

                # Caso a opção "Aperte para falar" esteja desativada, o assistente entrará 
                # em ação somente se o usuário falar seu nome.

                if not press_to_speak:

                    # Verifica se o usuário chamou o assistente.
                    if text.lower().find(name.lower()) == -1:
                        continue

                # Caso o usuário tenha chamado pelo assistente, será obtido o texto sem o nome dele.
                if text.lower().find(name.lower()) != -1:
                    text = text[text.lower().find(name.lower())+len(name)+1:]
                

                # Verifica se é um comando definido pelo usuário.
                userCommand = False

                for key in self.__userCommands.keys():
                    
                    # Se sim, o programa obtém as informações deste comando.
                    if text.lower() == key.lower():
                        command = self.__userCommands[key]
                        userCommand = True

                        # Verifica se o caminho do programa existe.
                        if os.path.exists(command["Path"]):

                            # Executa o programa.
                            file = os.path.split(command["Path"])[-1]
                            self.speak(name,'Starting "{}"...',language,[file,],sound=sounds)
                            self.__assistantCommands.start(command["Path"],command["Arguments"])

                        else:

                            # Informa que não foi possível executar o programa.
                            self.speak(
                                name,
                                "I'm sorry, but I can't run the program associated with this command.",
                                language,duration=3,wait=True,sound=sounds
                                )
                        break
                
                # Volta caso tenha sido executado um comando definido pelo usuário.
                if userCommand: 
                    continue

                # Comando 0 significa que não existe um comando do assistente para o pedido do usuário.
                command = 0

                # Tenta tranformar a primeira palavra (comando) do texto em um verbo no infinitivo.
                word = text.split(maxsplit=1)[0]
                verb = self.__translator.getVerbs(word,language,0)
                if verb:
                    text = text.replace(word,verb[0].lower())

                # Obtém uma chave para executar um comando do assistente.
                for key in self.__commands.keys():

                    if text.lower().find(key) == 0:
                        command = self.__commands[key]

                        # Separa o comando do resto do texto.
                        text = text[len(key)+1:]
                        break

                
                # Se o comando for "open", ele tentará abrir um programa, arquivo ou pasta 
                # com o nome que o usuário disse.
                if command == self.__defaultCommands["open"]:

                    try:
                        # Procura por um programa, arquivo ou pasta com o nome que o usuário disse.
                        path = self.__assistantCommands.find(text,paths.copy())
                        
                        # Informa que o programa está sendo aberto.
                        self.speak(name,'Starting "{}"...',language,[text,],sound=sounds)

                        # Abre o programa.
                        AssistantCommands.start(path,"")

                    except:
            
                        # Informa que não foi possível encontrar o programa.
                        self.speak(
                            name,"""I'm sorry, but I can't find "{}" on your computer.""",language,[text,],wait=True,sound=sounds
                            )

                # Se o comando for "go to", ele irá abrir o site no navegador. 
                # Caso não seja possível, ele irá pesquisar na internet pelo mesmo.
                elif command == self.__defaultCommands["go to"]:

                    # Informa que ele está pesquisando pelo site.
                    self.speak(name,'Searching for "{}"...',language,[text,],sound=sounds)
                    self.__assistantCommands.searchOnTheInternet(text)

                # Se o comando for "search", ele irá abrir o navegador com a busca.
                elif command == self.__defaultCommands["search"]:
                    
                    # Informa que ele está pesquisando na internet.
                    self.speak(name,'Searching for "{}"...',language,[text,],sound=sounds)   
                    self.__assistantCommands.searchOnTheInternet(text,False)

                # Se o comando for "calculate", ele irá tentar calcular uma expressão e dizer o resultado.
                elif command == self.__defaultCommands["calculate"]:
                    try:

                        # Tenta obter o resultado.
                        result = self.__assistantCommands.calculate(text)
                        
                        # Informa o resultado.
                        if int(result) != result:
                            self.speak(name,"The result is {}.",language,[str(result),],sound=sounds)
                        else:
                            self.speak(name,"The result is {}.",language,[str(int(result)),],sound=sounds)

                    except Exception:
                        # Informa que não foi possível realizar o cálculo.
                        self.speak(
                            name,"Oops, I can't seem to do that kind of calculation.",
                            language,wait=True,sound=sounds
                            )                

                # Se o comando for "add path", será aberto uma janela para o usuário definir um caminho.
                elif command == self.__defaultCommands["add path"]:

                    # Se o usuário selecionou um diretório para ser adicionado, esse diretório será salvo.
                    if self.__assistantCommands.addPath():
                        self.saveSettings(self.__settingsFile)
                        self.speak(name,"This directory has been successfully added to the system.",language,sound=sounds)


                # Se o comando for "remove path", será aberto uma janela para o usuário 
                # remover um diretório da lista de diretórios.
                elif command == self.__defaultCommands["remove path"]:

                    # Verifica se o usuário selecionou um diretório para ser deletado.
                    if self.__assistantCommands.deletePath():
                        self.saveSettings(self.__settingsFile)
                        self.speak(name,"This directory has been successfully deleted from the system.",language,sound=sounds)

                # Se o comando for "command list", será aberto uma janela com a lista de todos os comandos.
                elif command == self.__defaultCommands["command list"]:
                    self.help()

                # Se o comando for "minimize", uma janela do computador do usuário será minimizada.
                elif command == self.__defaultCommands["minimize"]:

                    # Caso não exista um nome, será minimizado a janela ativa.
                    if not text: text = None

                    # Caso exista um nome, será verificado se existe uma janela com este nome.
                    else:
                        if not self.__assistantCommands.isWindow(text):
                            self.speak(
                                name,"""I'm sorry,' but I can't find a window named "{}".""",[text],sound=sounds
                                )
                            return
                    self.__assistantCommands.minimizeProgram(title=text)

                # Se o comando for "maximize", uma janela do computador do usuário será maximizada.
                elif command == self.__defaultCommands["maximize"]:
                    if not text: return

                    # Verifica se existe uma janela com o nome que o usuário disse.
                    if not self.__assistantCommands.isWindow(text):
                        self.speak(name,"""I'm sorry,' but I can't find a window named "{}".""",[text],sound=sounds)
                    self.__assistantCommands.maximizeProgram(title=text)

                # Se o comando for "close", será fechado um programa do computador do usuário.
                elif command == self.__defaultCommands["close"]:

                    # Caso não exista um nome, será fechado a janela ativa.
                    if not text: 
                        text = None

                    # Caso exista um nome, será verificado se existe uma janela com este nome.    
                    else:
                        if not self.__assistantCommands.isWindow(text):
                            self.speak(
                                name,"""I'm sorry,' but I can't find a window named "{}".""",[text],sound=sounds
                                )
                            return
                    self.__assistantCommands.closeProgram(text)

                # Se o comando for "add command", será aberto uma janela para que o usuário defina um comando.
                elif command == self.__defaultCommands["add command"]:
                    self.__assistantCommands.setCommand(icon=self.__icon)

                # Se o comando for "edit command", será aberto uma janela para que o usuário edite um comando.
                elif command == self.__defaultCommands["edit command"]:

                    # Define título da janela para selecionar o comando.
                    title = self.__translator.translate("Select a command",language,"en").text

                    # Cria uma lista para que o usuário selecione o comando que ele deseja editar.
                    itemList = ItemList(title,width=40,height=10,icon=self.__icon,selection=True)
                    command = itemList.run(
                        [" "+key.capitalize() for key in self.__userCommands.keys()],
                        self.getStatus
                        )
                    # Caso um comando tenha sido selecionado, uma janela será aberta 
                    # com as informações deste comando para edição.
                    if command:
                        self.__assistantCommands.setCommand(self.__userCommands[command.lower()],icon=self.__icon)

                else:
                    # Informa que não foi possível executar nenhum comando.
                    self.speak(name,"I'm sorry, but I didn't understand what you said.",language,wait=True,sound=sounds)
        
        # Informa que acabou a execução do método.
        self.__running = False


    def save(self):
        """
        Método para savar todas as informações.
        """
        self.saveSettings()
        self.saveUserCommands()


    def saveSettings(self,settingsFile=None):
        """
        Método para salvar as configurações atuais do assistente.
        """
        
        if not settingsFile:
            settingsFile = self.__settingsFile

        # Cria diretório caso não exista.
        path = os.path.split(settingsFile)[0]
        if not os.path.exists(path):
            os.mkdir(path)
        
        # Salva o arquivo.
        with open(settingsFile,'w') as file:
            file.write(json.dumps(self.__settings,indent=2))


    def saveUserCommands(self,commandsFile=None):
        """
        Método para salvar os comandos criados pelo usuário.
        """

        if not commandsFile:
            commandsFile = self.__commandsFile

        # Cria diretório caso não exista.
        path = os.path.split(commandsFile)[0]
        if not os.path.exists(path):
            os.mkdir(path)
        
        # Salva o arquivo.
        with open(commandsFile,'w') as file:
            file.write(json.dumps(self.__userCommands,indent=2))


    def speak(self,title,text,language=None,substrings=None,duration=5,wait=False,sound=False):
        """
        Método para o assistente se comunicar com o usuário.
        """

        # Traduz a linguagem caso exista algo no parâmetro language.
        if language:
            try:
                msg = self.__translator.translate(text,language,self.__defaultLanguage.split("-")[0]).text
            except:
                msg = text
        else:
            msg = text

        # Adiciona substrings que não foram traduzidas.
        if substrings:
            msg = msg.format(*substrings)
        self.__messageBox.send(title=title,message=msg,duration=duration,threaded=True)

        # Executa um som de mensagem.
        if sound: self.__sounds.play_sound(self.__sounds.message_fn)

        # Aguarda a mensagem fechar para prosseguir.
        if wait:
            time.sleep(duration)


    def stop(self):
        """
        Encerra o método run().
        """
        self.__stop = True
        self.save()


