import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
TEMPLATE_DIR = os.path.join(ROOT_DIR, "template")


class Colors:
    """
    Color constants
    """
    BLACK = "#121213"
    LIGHT_GRAY = "#818384"
    DARK_GRAY = "#3a3a3c"
    YELLOW = "#b49f3b"
    GREEN = "#548d4e"
    WHITE = "#d8dadc"
