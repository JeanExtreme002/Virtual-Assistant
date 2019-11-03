from win10toast import ToastNotifier

class MessageBox(object):

    def __init__(self,icon=None):
        
        self.__icon = icon
        self.__toastNotifier = ToastNotifier()


    def send(self,title,message,duration=5,threaded=False):

        self.__toastNotifier.show_toast(
            title,
            message,
            icon_path=self.__icon,
            duration=duration,
            threaded=threaded
        )
