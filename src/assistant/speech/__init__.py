from .listener import Listener
from .speaker import Speaker

__all__ = ("Speech",)

class Speech(Listener, Speaker):
    pass
