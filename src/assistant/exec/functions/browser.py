import webbrowser

def search_on_google(search):
    webbrowser.open("https://www.google.com/search?q=" + search.replace(" ", "%20"))
