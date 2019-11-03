from tkinter import Listbox,Scrollbar,Tk

class ItemList(object):

    def __init__(self,title,width=115,height=10,bg="white",fg="black",font=("Consolas",10),icon=None,selection=False):

        # Cria janela.
        self.__root = Tk()

        # Configura a janela.
        self.__root.resizable(False,False)
        self.__root.title(title)
        self.__root.iconbitmap(icon)
        self.__root.focus_force()

        # Cria uma barra de rolagem.
        scrollbar = Scrollbar(self.__root)
        scrollbar.pack(side="right",fill="y")

        # Cria lista de itens.
        self.__listbox = Listbox(self.__root,width=width,height=height,font=font)
        self.__listbox.config(yscrollcommand=scrollbar.set)
        self.__listbox.pack()

        # Configura a barra de rolagem.
        scrollbar.config(command=self.__listbox.yview)

        # Desativa o mecanismo de seleção da lista caso "selection" seja False.
        if not selection:
            self.__listbox.bindtags((self.__listbox, self.__root, "all"))
        else:
            self.__listbox.config(selectmode="SINGLE")
        self.__selection = selection


    def __close(self,event):
        """
        Método do evento para fechar janela.
        """
        self.__root.destroy()


    def run(self,list_,stopFunction,spacing=30):
        """
        Coloca as strings dentro da lista e a executa dentro de um mainloop.
        """

        # Evento para fechar a janela.
        self.__stopFunction = stopFunction
        self.__root.bind("<Escape>",self.__close)

        # Coloca os itens dentro da lista.
        for item in list_:

            # Caso tenha sido definido um espaçamento, será separado o título da descrição.
            if spacing and not isinstance(item,str):
                if len(item[0]) < spacing:
                    item[0] += " "*(spacing-len(item[0]))
                else:
                    item[0] = item[0][:spacing-3]+"..."
                self.__listbox.insert(0,item[0] + "   "+ item[1])
            
            # Caso não tenha sido definido um espaçamento, será colocado simplesmente o item à lista.
            else:
                self.__listbox.insert(0,item)

        # Atualiza a janela.
        self.__item = None
        self.__updater()
        self.__root.mainloop()

        # Retorna um item selecionado.
        return self.__item

    
    def __updater(self):
        """
        Método para obter um item selecionado e verificar se o usuário deseja fechar a janela.
        """

        # Obtém um item selecionado.
        if self.__selection:
            item = self.__listbox.curselection()
            if item:
                self.__item = self.__listbox.get(item[0]).strip()
                self.__root.destroy()

        # Caso o retorno da função seja True, ele irá parar de atualizar a janela.
        if not self.__stopFunction():
            return self.__root.after(1,self.__updater)
        else:
            self.__root.destroy()

