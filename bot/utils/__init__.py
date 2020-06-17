from .aliases import Aliases
from .config import Config
from .servers import Servers

config = Config()
servers = Servers()
aliases = Aliases()


__all__ = ["config", "servers", "aliases"]
