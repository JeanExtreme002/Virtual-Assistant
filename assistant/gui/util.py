from PIL import Image,ImageTk
from tkinter import Canvas,Entry,Frame,Label,Text,Tk
from tkinter.ttk import Button,Style
from tkinter.filedialog import askdirectory,askopenfilename


class CommandForm():
    def __init__(self,command="",args="",description="",**kw):
        """
        Função para obter [comando,parâmetros,diretório_do_programa].
        """

        # Configurações dos widgets.
        settings = {
            "window_icon":None,
            "window_title":"Set Command",
            "window_width":550,
            "window_height":250,
            "window_bg":"white",
            "entry_titles":[" Command: "," Arguments: ","Description"],
            "entry_bg":"#F5F5F5",
            "entry_fg":"black",
            "entry_font":("Arial",15),
            "entry_width":50,
            "button_text":"Add",
            "button_width":20,
            "button_font":("Arial",12),
            "text_text":description,
            "text_font":None,
            "text_fg":"black",
            "text_bg":"#DCDCDC",
            "text_width":60,
            "text_height":7
        }
        settings.update(kw)

        # Cria janela.
        root = Tk()
        root.geometry("%ix%i"%(settings["window_width"],settings["window_height"]))
        root.title(settings["window_title"])
        root.resizable(False,False)
        root.iconbitmap(settings["window_icon"])
        root["bg"] = settings["window_bg"]

        # Cria frame para inserir o comando.
        command_entry_frame = Frame(root,bg=settings["window_bg"])
        command_entry_frame.pack()

        # Cria título e entry.
        Label(
            command_entry_frame,
            text=settings["entry_titles"][0],
            bg=settings["entry_bg"],
            fg=settings["entry_fg"],
            font=settings["entry_font"],
            borderwidth=1, relief="groove"
            ).pack(side="left")

        command_entry = Entry(
            command_entry_frame,
            width=settings["entry_width"],
            bg=settings["entry_bg"],
            fg=settings["entry_fg"],
            font=settings["entry_font"]
            )
        command_entry.insert(0,command)
        command_entry.focus_force()
        command_entry.pack(side="left")

        # Faz com que não seja mais possível mover os widgets da esquerda para direita.
        Label(command_entry_frame,bg=settings["window_bg"],width=300).pack(side="right")

        #===========================================================================================

        # Cria frame e widgets para inserir os parâmetros que serão passados ao executar o programa.
        args_entry_frame = Frame(root,bg=settings["window_bg"],pady=2)
        args_entry_frame.pack()

        # Cria título e entry.
        Label(
            args_entry_frame,
            text=settings["entry_titles"][1],
            bg=settings["entry_bg"],
            fg=settings["entry_fg"],
            font=settings["entry_font"],
            borderwidth=1, relief="groove"
            ).pack(side="left")

        args_entry = Entry(
            args_entry_frame,
            width=settings["entry_width"],
            bg=settings["entry_bg"],
            fg=settings["entry_fg"],
            font=settings["entry_font"]
            )
        args_entry.insert(0,args)   
        args_entry.pack(side="left")

        # Faz com que não seja mais possível mover os widgets da esquerda para direita.
        Label(args_entry_frame,bg=settings["window_bg"],width=300).pack(side="right")

        #===========================================================================================

        # Cria título e um espaço para colocar uma descrição para o comando.
        Label(
            root,
            text=settings["entry_titles"][2],
            bg=settings["window_bg"],
            fg=settings["entry_fg"],
            font=settings["entry_font"],
            ).pack()

        description= Text(
            root,
            width=settings["text_width"],
            height=settings["text_height"],
            bg=settings["text_bg"],
            fg=settings["text_fg"],
            font=settings["text_font"]
            )
        description.insert(0.0,settings["text_text"])
        description.pack()


        # Cria um botão.
        style = Style()
        style.configure("TButton",width=settings["button_width"],font=settings["button_font"])
        button = Button(root,text=settings["button_text"],command=self.__addCommand,style="TButton")
        button.pack(pady=5)


        # Atributos que guardarão as informações do comando.
        command_entry.text = None
        args_entry.text = None
        description.text = None

        self.__command_entry = command_entry
        self.__args_entry = args_entry
        self.__description = description
        self.__root = root
        self.__added = False


    def __addCommand(self):
        """
        Função do botão para adicionar um comando.
        """

        # Adiciona o comando apenas se o usuário tiver colocado algo na entry de comando.
        if self.__command_entry.get():

            # Obtém informações do comando.
            self.__command_entry.text = self.__command_entry.get()
            self.__args_entry.text = self.__args_entry.get()
            self.__description.text = self.__description.get(0.0,"end").replace("\n"," ").strip()

            # Obtém um programa para executar com o comando que o usuário definiu.
            self.__path = askopenfilename()
            if not self.__path: return

            # Fecha a janela e informa que o comando foi adicionado.
            self.__root.destroy()
            self.__added = True


    def __close(self,event):
        """
        Método do evento para fechar janela.
        """
        # Fecha a janela.
        self.__root.destroy()


    def run(self,stopFunction=None):

        # Evento para fechar a janela.
        self.__root.bind("<Escape>",self.__close)

        # Atualiza a janela.
        if stopFunction: 
            self.__stopFunction = stopFunction
            self.__updater()
        self.__root.mainloop()

        # Retorna as informações.
        if self.__added: 
            return [self.__command_entry.text,self.__args_entry.text,self.__description.text,self.__path]


    def __updater(self):

        # Fecha a janela caso o usuário tenha apertado 
        # no botão para adicionar ou tenha solicitado o fechamento.
        if not self.__stopFunction() and not self.__added:
            self.__root.after(10,self.__updater)

        elif not self.__added:
            self.__root.destroy()



def getCommand(command="",args="",description="",stopFunction=None,**kw):
    """
    Função para obter um comando no formato [command,args,description,path].
    """
    cf =  CommandForm(command=command,args=args,description=description,**kw)
    return cf.run(stopFunction=stopFunction)



def getDirectory():
    """
    Função para obter um diretório.
    """
    root = Tk()
    root.withdraw()
    path = askdirectory(parent=root)
    root.destroy()
    return path



def getFilename():
    """
    Função para obter um nome de arquivo.
    """
    root = Tk()
    root.withdraw()
    path = askopenfilename(parent=root)
    root.destroy()
    return path
