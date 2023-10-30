from pathlib import Path

# Constantes
BASE_NOTEBOOK_PATH = Path("/home/listserv/lists/archives")
MAX_LINE_LENGTH = 80

# Contenu commun pour toutes les listes
COMMON_HEADER_CONTENT = ["*", "*", "*", "* .HH ON"]
COMMON_CONTENT = [
    "* Ack= Yes",
    "* Attachments= Yes",
    "* Auto-Delete= Yes,Semi-Auto,Delay(4),Max(6),Probe(30)",
    "* Change-Log= Yes",
    "* Confidential= Yes",
    "* Errors-To= Owners",
    "* Language= FRANCAIS",
    "* Loopcheck= NoSpam",
    "* Misc-Options= UTF8_HEADER",
    "* Notify= Yes",
    "* Sender= None",
    "* Service= *",
    "* Subscription= By_Owner",
    "* Validate= No"
]
COMMON_FOOTER_CONTENT = ["* .HH OFF", "*"]
