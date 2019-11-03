
__author__ = "Jean Loui Bernard Silva de Jesus"

import sys
if not "win" in sys.platform: quit()

from assistant import Assistant
from assistant.gui.messageBox import MessageBox
from infi.systray import SysTrayIcon 
import time
import os 


icon = "images/icon.ico"
trayIcon_title = "Virtual Assistant"
va_settingsPath = "data"

# Cria uma intância de MessageBox para enviar mensagens para o usuário.
messageBox = MessageBox(icon)

# Obtém uma instância de Assistant e um objeto responsável pelas suas ações.
assistant = Assistant(messageBox,va_settingsPath,icon=icon)
assistantCommands = assistant.getAssistantCommands()

# Obtém um tradutor.
translator = assistant.getTranslator()


def changeLanguage(systray):
    """
    Função para trocar o idioma do assistente.
    """

    language = assistantCommands.changeLanguage()
    trayIcon.update(hover_text=trayIcon_title+" (%s)"%language)

def enable_sounds(systray):
    """
    Função para habilitar os sons do programa.
    """
    assistantCommands.enable_or_disable_sounds(True)

def disable_sounds(systray):
    """
    Função para desabilitar os sons do programa.
    """
    assistantCommands.enable_or_disable_sounds(False)

def help_(systray):
    """
    Função para abrir janela com os comandos do assistente.
    """
    global icon
    assistantCommands.help()

def hideInput(systray):
    """
    Função para não mostrar o que o usuário falar em formato de texto.
    """
    assistantCommands.hide_or_show_input(False)

def showInput(systray):
    """
    Função para mostrar o que o usuário falar em formato de texto.
    """
    assistantCommands.hide_or_show_input(True)

def quit_(systray):
    """
    Função para fechar o programa.
    """
    assistant.stop()


# Define o menu do ícone de bandeja.
menu = (
    ("Change Language",None,changeLanguage),
    ("Enable Sounds",None,enable_sounds),
    ("Disable Sounds",None,disable_sounds),
    ("Hide Input",None,hideInput),
    ("Show Input",None,showInput),
    ("Help",None,help_)
)

# Cria um ícone de bandeja.
trayIcon = SysTrayIcon(icon,trayIcon_title+" (%s)"%assistant.getLanguage().upper(),menu,on_quit=quit_)
trayIcon.start()

# Inicia o assistente.
assistant.run()

# Fecha o programa por completo.
time.sleep(1)
os._exit(0)
