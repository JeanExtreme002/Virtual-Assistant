from ..parser.command import Command

reserved_commands = {
    "en-us": {
        "close window": Command(
            system_command = "close window",
            info = "Closes a window by its title",
            exec_message = "",
            success_message = "",
            error_message = "Sorry, but I couldn't find the window \"{args}\""
        ),
        "close": Command(
            system_command = "close",
            info = "Closes the active window",
            exec_message = "",
            success_message = "",
            error_message = ""
        ),
        "maximize window": Command(
            system_command = "maximize window",
            info = "Maximizes a window by its title",
            exec_message = "",
            success_message = "",
            error_message = "Sorry, but I couldn't find the window \"{args}\""
        ),
        "maximize": Command(
            system_command = "maximize",
            info = "Maximizes the active window",
            exec_message = "",
            success_message = "",
            error_message = ""
        ),
        "minimize window": Command(
            system_command = "minimize window",
            info = "Minimizes a window by its title",
            exec_message = "",
            success_message = "",
            error_message = "Sorry, but I couldn't find the window \"{args}\""
        ),
        "minimize": Command(
            system_command = "minimize",
            info = "Minimizes the active window",
            exec_message = "",
            success_message = "",
            error_message = ""
        ),
        "open folder": Command(
            system_command = "open folder",
            info = "Opens a folder",
            exec_message = "Looking for \"{args}\" ...",
            success_message = "",
            error_message = "I'm sorry, but I couldn't find the folder \"{args}\""
        ),
        "open file": Command(
            system_command = "open file",
            info = "Opens a file",
            exec_message = "Looking for \"{args}\" ...",
            success_message = "",
            error_message = "I'm sorry, but I couldn't find the file \"{args}\""
        ),
        "open": Command(
            system_command = "open",
            info = "Opens a program",
            exec_message = "Looking for \"{args}\" ...",
            success_message = "",
            error_message = "I'm sorry, but I couldn't find the program \"{args}\""
        ),
        "repeat": Command(
            system_command = "repeat",
            info = "Repeat what was said",
            exec_message = "",
            success_message = "{output}",
            error_message = ""
        ),
        "search": Command(
            system_command = "search",
            info = "Performs a search on the web",
            exec_message = "Searching for \"{args}\" ...",
            success_message = "",
            error_message = ""
        ),
        "show ip": Command(
            system_command = "show ip",
            info = "Shows the private IP",
            exec_message = "",
            success_message = "Your private IP is \"{output}\"",
            error_message = ""
        ),
        "show public ip": Command(
            system_command = "show public ip",
            info = "Shows the public IP",
            exec_message = "",
            success_message = "Your public IP is \"{output}\"",
            error_message = ""
        ),
        "write": Command(
            system_command = "write",
            info = "Converts the speech to text",
            exec_message = "",
            success_message = "",
            error_message = ""
        )
    },
    "pt-br": {
        "abrir pasta": Command(
            system_command = "open folder",
            info = "Abre uma pasta",
            exec_message = "Procurando por \"{args}\" ...",
            success_message = "",
            error_message = "Sinto muito, mas eu não consegui encontrar a pasta \"{args}\""
        ),
        "abrir arquivo": Command(
            system_command = "open file",
            info = "Abre um arquivo",
            exec_message = "Procurando por \"{args}\" ...",
            success_message = "",
            error_message = "Desculpe, mas eu não consegui encontrar o arquivo \"{args}\""
        ),
        "abrir": Command(
            system_command = "open",
            info = "Executa um programa",
            exec_message = "Procurando por \"{args}\" ...",
            success_message = "",
            error_message = "Lamento, mas eu não consegui encontrar o programa \"{args}\""
        ),
        "escreva": Command(
            system_command = "write",
            info = "Converte a fala para texto",
            exec_message = "",
            success_message = "",
            error_message = ""
        ),
        "fechar janela": Command(
            system_command = "close window",
            info = "Fecha uma janela pelo seu título",
            exec_message = "",
            success_message = "",
            error_message = "Desculpe, mas eu não consegui encontrar a janela \"{args}\""
        ),
        "fechar": Command(
            system_command = "close",
            info = "Fecha a janela ativa",
            exec_message = "",
            success_message = "",
            error_message = ""
        ),
        "maximizar janela": Command(
            system_command = "maximize window",
            info = "Maximiza uma janela pelo seu título",
            exec_message = "",
            success_message = "",
            error_message = "Desculpe, mas eu não consegui encontrar a janela \"{args}\""
        ),
        "maximizar": Command(
            system_command = "maximize",
            info = "Maximiza a janela ativa",
            exec_message = "",
            success_message = "",
            error_message = ""
        ),
        "minimizar janela": Command(
            system_command = "minimize window",
            info = "Minimiza uma janela pelo seu título",
            exec_message = "",
            success_message = "",
            error_message = "Desculpe, mas eu não consegui encontrar a janela \"{args}\""
        ),
        "minimizar": Command(
            system_command = "minimize",
            info = "Minimiza a janela ativa",
            exec_message = "",
            success_message = "",
            error_message = ""
        ),
        "mostrar ip": Command(
            system_command = "show ip",
            info = "Mostra o IP privado",
            exec_message = "",
            success_message = "O seu IP privado é \"{output}\"",
            error_message = ""
        ),
        "mostrar ip público": Command(
            system_command = "show public ip",
            info = "Mostra o IP público",
            exec_message = "",
            success_message = "O seu IP público é \"{output}\"",
            error_message = ""
        ),
        "pesquisar": Command(
            system_command = "search",
            info = "Realiza uma pesquisa na internet",
            exec_message = "Pesquisando por \"{args}\" ...",
            success_message = "",
            error_message = ""
        ),
        "repetir": Command(
            system_command = "repeat",
            info = "Repete o que foi dito",
            exec_message = "",
            success_message = "{output}",
            error_message = ""
        ),
    }
}
