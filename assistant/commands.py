from assistant.gui import util
from assistant.gui.itemList import ItemList
from subprocess import check_call
from threading import Thread
import math
import os
import psutil
import pygetwindow
import re
import requests


class SystemCommands(object):

    internetDomains = [".com",".org",".net",".tv"]
    searchUrl = "https://www.google.com/search?q="

    def __init__(self):

        self.partition = psutil.disk_partitions()[0].device
        self.user = os.getlogin()
        self.publicDesktop = os.path.normpath("{}Users/Public/Desktop".format(self.partition))
        self.desktop = os.path.normpath("{}Users/{}/Desktop".format(self.partition,self.user))


    @staticmethod
    def closeProgram(hWnd=None,title=None):
        """
        Método para fechar um programa.
        """

        window = SystemCommands.getWindow(hWnd,title)
        if window:
            window.close()  


    def find(self,name,paths=[],all_=False):
        """
        Método para procurar programa, arquivo ou pasta
        com o nome definido no parâmetro "name".

        Este método dá preferência a arquivos com extensões ".exe" e ".lnk".
        Caso não seja encontrado arquivo com uma dessas extensões, será retornado 
        o primeiro arquivo encontrado. Caso não seja encontrado nenhum arquivo,
        será retornado o primeiro diretório encontrado com este nome.
        """

        # Essa listá irá conter arquivos encontrados porém 
        # que não são executáveis ou atalhos de programas.
        apps = []
        dirs = []

        # Adiciona à lista de diretórios para busca o diretório atual, o public desktop e o user desktop. 
        paths.append(os.getcwd())
        paths.append(self.publicDesktop)
        paths.append(self.desktop)

        # Adiciona à lista de diretórios para busca os caminhos definidos na variável de ambiente PATH.
        for path in os.environ["PATH"].split(";"):
            paths.append(path)

        # Percorre cada diretório.
        for path in paths:

            try:
                dirList = os.listdir(path)
            except:
                continue

            # Percorre cada arquivo do diretório verificando existe um programa de X nome para ser retornado.
            for file in dirList:
                
                # Verifica se o nome do item é o mesmo da variável "name".
                if name.lower() == os.path.splitext(file.lower())[0]:

                    # Verifica se ele é um diretório ou não.
                    if not os.path.isdir(path+"/"+file):

                        # Se o arquivo acabar com a extensão ".exe" ( executável ) 
                        # ou ".lnk" (atalho de programa), o mesmo será retornado.
                        if file.endswith(".exe") or file.endswith(".lnk"):

                            if all_:
                                apps.append(path+"/"+file)
                            else:
                                return path+"/"+file

                        # Se não for o caso, o arquivo será adicionado à lista de arquivos encontrados.
                        else:
                            apps.append(path+"/"+file)
                    else:
                        dirs.append(path+"/"+file)
 

        # Retorna todos os arquivos e pastas encontrados.
        if all_:
            results = apps.extend(dirs)
            if not results:
                raise FileNotFoundError
            else:
                return results

        # Caso não tenha sido encontrado nenhum arquivo com as extensões ".exe" ou "lnk", 
        # será retornado o primeiro arquivo encontrado.
        # Caso ele não tenha encontrado nenhum arquivo, será retornado o primeiro diretório encontrado.

        if len(apps) > 0:
            return apps[0]
        else:
            if len(dirs) > 0:
                return dirs[0]
            else:
                raise FileNotFoundError
    

    @staticmethod
    def getWindow(hWnd=None,title=None):
        """
        Método para obter uma instância de pygetwindow.Window.
        """

        # Caso tenha sido passado um hWnd, será retornado uma instância através dele.
        if isinstance(hWnd,int):
            window = pygetwindow.Window(hWnd)

        # Caso tenha sido passado um título, será retornado uma instância utilizando o título.
        elif title and isinstance(title,str):

            # Para que não haja muitos problemas, letras maiúsculas e minúsculas 
            # não farão diferença para obter uma janela.
            for title_ in pygetwindow.getAllTitles():
                if title_.lower() == title.lower():
                    title = title
                    break

            window = pygetwindow.getWindowsWithTitle(title)[0]

        # Caso não tenha sido passado um título, será retornando uma instância da janela ativa.
        else:
            window = pygetwindow.getActiveWindow()
        
        # Retorna a janela.
        return window


    @staticmethod
    def isWindow(title):
        """
        Verifica se existe uma janela como determinado título, 
        não fazendo diferença entre letras maiúsculas ou minúsculas.
        """
        for title_ in pygetwindow.getAllTitles():
            if title_.lower() == title.lower(): return True


    @staticmethod
    def maximizeProgram(hWnd=None,title=None):
        """
        Método para maximizar uma janela.
        """

        window = SystemCommands.getWindow(hWnd,title)
        if window:
            window.maximize() 


    @staticmethod
    def minimizeProgram(hWnd=None,title=None):
        """
        Método para minimizar uma janela.
        """

        window = SystemCommands.getWindow(hWnd,title)
        if window:
            window.minimize()  
             


    def searchOnTheInternet(self,search,goToWebSite=True):
        """
        Método para realizar uma pesquisa na internet.
        """
        
        # Percorre cada domínio da lista.
        for domain in self.internetDomains:
            if not goToWebSite: break
            

            # Caso a pesquisa seja um link, será verificado se o site desse link existe.
            if "." in search:
                
                # Tenta realizar uma conexão.
                try:
                    r = requests.get("http://"+search.replace(" ",""),timeout=3)
                except: break

                # Verifica se o site existe. Se sim, ele será aberto no navegador do usuário.
                if r.status_code != 404:
                    check_call("start http://"+search.replace(" ",""),shell=True)

                # Caso não seja encontrado um site para a busca, será aberto o navegador com a pesquisa na Google.
                else:
                    check_call("start "+self.searchUrl+search.replace(" ","%20"),shell=True)
                return


            # Tenta realizar uma conexão.
            try:
                r = requests.get("http://"+search.replace(" ","")+domain)
            except: continue

            # Verifica se o site existe. Se sim, ele será aberto no navegador do usuário.
            if r.status_code != 404:
                check_call("start http://%s%s"%(search.replace(" ",""),domain),shell=True)
                return
        
        # Caso não seja encontrado um site para a busca, será aberto o navegador com a pesquisa na Google.
        check_call("start "+self.searchUrl+search.replace(" ","%20"),shell=True)


    @staticmethod
    def start(name,args):
        """
        Método para abrir um programa, arquivo ou diretório. 
        Você pode também passar argumentos para o mesmo. Exemplo:

        >>> start("app.exe","user=User32_Bot password=mickey23")

        Isso equivale a fazer no CMD: start app.exe user=User32_bot password=mickey23
        """

        check_call('start "" "%s" %s'%(os.path.normpath(name),args),shell=True)



class AssistantCommands(SystemCommands):
    """
    Classe responsável pelas ações do assistente.
    """

    __languages = ["EN-US","PT-BR"]
    __language = 0
    __open_commandList = False


    def __init__(self,assistant,settings,commands):

        SystemCommands.__init__(self)
        self.__assistant = assistant
        self.__translator = assistant.getTranslator()
        self.__settings = settings
        self.__commands = commands
        self.__language = self.__languages.index(assistant.getLanguage().upper())


    def addPath(self):
        """
        Método para adicionar um caminho para o 
        assistente realizar buscas e outros.
        """

        path = util.getDirectory()
        if path:
            self.__settings["System"]["Paths"].append(path)
            return 1
        else:
            return 0


    def calculate(self,expression):
        """
        Método para calcular uma expressão com operações simples de matemática.

        É permitido na expressão conter os seguintes itens: 
        - Adição 
        - Subtração 
        - Multiplicação 
        - Divisão 
        - Fatorial
        - Raiz quadrada
        - Seno
        - Cosseno
        - Tangente
        - PI
        """

        def format_expression(string,functions):
            """
            Função para formatar uma expressão aritmética.
            """

            for function_format in functions:

                # Procura pelas funções na string.
                found_functions = re.findall(function_format[0],string)
                if not found_functions: continue
            
                # Formata todas as funções encontradas.
                for math_function in found_functions:

                    # Obtém o valor a ser passado.
                    value = re.findall("\\d+",math_function)
                    if not value: continue
                    string = string.replace(math_function,function_format[1]+"({})".format(value[0]))

            # Retorna a string formatada.
            return string

        # Obtém a linguagem de origem.
        language = self.__assistant.getLanguage().split("-")[0]
   
        # Aplica um espaçamento nos operadores aritméticos.
        expression = expression.replace("-"," - ")
        expression = expression.replace("/"," / ")
        expression = expression.replace("+"," + ")
        expression = expression.replace("*"," * ")

        # Palavras que serão ignoradas na expressão.
        ignore = ["the","calculator","calculate","compute","please","by","for"]

        new_expression = ""
        substring = ""
        index = -1
        
        # Percorre cada substring da string
        for string in expression.lower().split():
            
            # Traduz a expressão em partes, de forma que ele irá separar as partes pelos operadores aritméticos. 
            # Exemplo: Se a string for "fatorial de 5 + raiz quadrada de 16", será traduzida a parte "fatorial de 5"
            # e depois será traduzida a parte "raiz quadrada de 16". Por fim, as partes traduzidas serão juntadas.
            # Esse código de dividir a expressão em partes serve para evitar traduções incorretas.


            # Verifica se a string é uma operação aritmética.
            s = self.__translator.translate(string,"en",language).text.lower()
            index += 1

            if s == "multiplied":
                string = " * "
            elif s == "divided":
                string = " / "
            elif s == "plus":
                string = " + "
            elif string == "minus":
                string = " - "
            elif s in ignore:
                continue
            
            # Verifica se a string é um operador aritmético ou não. 
            # Se for, a substring será traduzida e será limpada para guardar uma outra parte da expressão.
            if not string in ["x","*","/","-","+"]:
                
                # Coloca a string junto com as outras strings que não são operadores aritméticos.
                substring += string + " "

                # Caso seja a última string da lista, ela será traduzida e juntada com as outras.
                if index == len(expression.split())-1:
                    new_expression += " "+self.__translator.translate(substring[:-1],"en",language).text
            else:

                # Traduz a substring adicionando no final o seu operador aritmético. Depois a substring traduzida
                # será adicionada à variável que terá a expressão traduzida e a mesma será apagada.
                
                if substring:
                    substring = self.__translator.translate(substring,"en",language).text
                new_expression += " "+ substring + " " + string
                substring = ""

        # Obtém a expressão traduzida.
        expression = new_expression.lower()
        
        for i in ignore:
            expression = expression.replace(i,"")

        # Funções que serão formatas.
        functions = [
            (
                "\\d+ factorial|factorial of \\d+|\\d+!",
                "square root of \\d+",
                "cos \\d+|cosine \\d+|cosine of \\d+|\\d+ cosine",
                "sin \\d+|sine \\d+|sine of \\d+|\\d+ sine",
                "tan \\d+|tangent \\d+|tangent of \\d+|\\d+ tangent"
                ),
            (
                "math.factorial",
                "math.sqrt",
                "math.cos",
                "math.sin",
                "math.tan"
                )
            ]

        # Formata a expressão, exemplo: "5 + 4 factorial" transforma-se em "5 + math.factorial(4)"
        expression = format_expression(expression,zip(functions[0],functions[1]))
        expression = expression.replace("pi",str(math.pi))
        expression = expression.replace("/"," / ")
        expression = expression.replace("+"," + ")
        expression = expression.replace("-"," - ")
        expression = expression.replace("*"," * ")
        expression = expression.replace("x"," * ")
        expression = expression.strip()

        if not expression: raise ValueError()

        # Verifica se há alguma string que não seja permitida e que possa afetar a segurança do programa.
        for char in expression.split():
            
            # Verifica se a string é um número ou um operador aritmético.
            if char.replace(".","").isnumeric(): continue
            elif char.replace(" ","") in ["*","/","-","+"]: continue

            isFunction = False

            # Verifica se a string é uma função.
            for function in functions[1]:
                if char.startswith(function):
                    isFunction = True
                    break
            # Caso a string não seja um número, operador aritmético ou função, será lançado um erro.
            if not isFunction:
                raise ValueError() 

        # Retorna o cálculo da expressão.
        return eval(expression)


    def changeLanguage(self):
        """
        Método para alterar o idioma do assistente.
        """

        # Obtém o próximo idioma.
        self.__language += 1
        if self.__language >= len(self.__languages):
            self.__language = 0
        language = self.__languages[self.__language]

        # Troca o idioma do assistente e salva as configurações.
        self.__assistant.changeLanguage(language)
        self.__assistant.saveSettings()
        return language


    def deletePath(self):
        """
        Método para deletar um caminho que o assistente 
        antes usava para realizar buscas e outros.
        """
        
        path = util.getDirectory()
        if path in self.__settings["System"]["Paths"]:
            self.__settings["System"]["Paths"].remove(path)
            return 1
        else:
            return 0


    def enable_or_disable_sounds(self,bool_):
        """
        Método para habilitar ou desabilitar os sons do assistente.
        """
        if type(bool_) is bool:
            self.__settings["System"]["Sounds"] = bool_
            self.__assistant.saveSettings()


    def help(self):
        """
        Método para mostrar ao usuário uma lista com todos 
        os comandos que o assistente possui.
        """
        self.__assistant.help()
        

    def hide_or_show_input(self,bool_=None):
        """
        Método para mostrar ou não o que o 
        usuário disse em formato de texto.
        """
        if type(bool_) is bool:
            self.__settings["System"]["ShowInput"] = bool_
        else:
            self.__settings["System"]["ShowInput"] = not self.__settings["System"]["ShowInput"]
        self.__assistant.saveSettings()


    def setCommand(self,command=None,icon=None):
        """
        Método para adicionar ou editar um comando.
        """

        # Obtém o idioma atual do assistente.
        language = self.__assistant.getLanguage().split("-")[0]

        # Define os títulos de cada caixa de informação.
        titles = [
            " "+self.__translator.translate("Command",language,"en").text.capitalize()+": ",
            " "+self.__translator.translate("Arguments",language,"en").text.capitalize()+": ",
            " "+self.__translator.translate("Description",language,"en").text.capitalize()+": ",
        ]
        # Caso haja um command, o mesmo será sobreescrito.
        if command:
            new_command = util.getCommand(
                command["Command"].capitalize(),
                command["Arguments"],
                command["Description"].capitalize(),
                stopFunction=self.__assistant.getStatus,
                entry_titles=titles,
                window_icon=icon,
                window_title=self.__translator.translate("Edit Command",language,"en").text,
                button_text=self.__translator.translate("Edit",language,"en").text
                )

        # Caso não haja um command, será criado um novo comando.
        else:
            new_command = util.getCommand(
                stopFunction=self.__assistant.getStatus,
                entry_titles=titles,
                window_icon=icon,
                window_title=self.__translator.translate("Add Command",language,"en").text,
                button_text=self.__translator.translate("Add",language,"en").text.split(",")[0]
                )

        # Caso o usuário tenha inserido todas as informações necessárias 
        # para criar ou editar um comando, o mesmo será salvo.
        if new_command:
            if command:
                self.__commands.pop(command["Command"].lower())

            self.__commands[new_command[0].strip().lower()] = {
                "Command":new_command[0].strip().capitalize(),
                "Arguments":new_command[1],
                "Description":new_command[2],
                "Path":new_command[3]
                }
            self.__assistant.saveUserCommands()

