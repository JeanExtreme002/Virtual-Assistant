import requests
import socket
import webbrowser

def get_private_ip():
    return socket.gethostbyname(socket.gethostname())

def get_public_ip():
    return requests.get("https://api.ipify.org").text

def search_on_google(search):
    webbrowser.open("https://www.google.com/search?q=" + search.replace(" ", "%20"))
