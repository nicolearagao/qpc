"""File to hold release constants."""
import os
from . import __package__version__

VERSION = __package__version__
AUTHOR = "QPC Team"
AUTHOR_EMAIL = "qpc@redhat.com"
QPC_VAR_PKG_SOURCE = os.environ.get("QPC_VAR_PKG_SOURCE", "qpc")
ENTRYPOINT = f"{QPC_VAR_PKG_SOURCE}=qpc.__main__:main"
URL = "https://github.com/quipucords/qpc"
