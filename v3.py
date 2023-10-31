from pathlib import Path
from enum import Enum

class ListType(Enum):
    PROTO_STD = "proto-std"
    PROTO_STD_ARCH = "proto-std-arch"
    PROTO_DISTR = "proto-distr"
    PROTO_MODR = "proto-modr"


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


class ListFileWriter:
    """Classe pour écrire le contenu de la liste dans un fichier."""

    @staticmethod
    def save(filename, content):
        try:
            with open(filename, 'w') as f:
                f.write('\n'.join(content))
        except Exception as e:
            print(f"Erreur lors de l'écriture dans le fichier {filename}: {e}")


# from constants import MAX_LINE_LENGTH, COMMON_HEADER_CONTENT, COMMON_CONTENT, COMMON_FOOTER_CONTENT, BASE_NOTEBOOK_PATH
from pathlib import Path
from enum import Enum

class ListType(Enum):
    PROTO_STD = "proto-std"
    PROTO_STD_ARCH = "proto-std-arch"
    PROTO_DISTR = "proto-distr"
    PROTO_MODR = "proto-modr"



class ProtoConfig:
    """Classe de base représentant une configuration prototype."""

    def __init__(self, description, owners, has_notebook=False):
        self._description = description
        self._owners = owners
        self._editors = []
        self._moderators = []
        self._has_notebook = has_notebook

    def _group_emails_in_lines(self, label, emails):
        """Groupe les e-mails en lignes avec une longueur maximale."""
        lines = []
        current_line = label
        for email in emails:
            if len(current_line + email + ",") > MAX_LINE_LENGTH:
                lines.append(current_line[:-1])
                current_line = label + email + ","
            else:
                current_line += email + ","
        lines.append(current_line[:-1])
        return lines

    def generate_content(self, filename):
        list_name = Path(filename).stem
        list_name_upper = list_name.upper()
        subject_tag = f'* Subject-Tag= "{list_name_upper}"'
        owner_content = self._group_emails_in_lines("* Owner= ", self._owners)
        editor_content = self._group_emails_in_lines("* Editor= ", self._editors) if self._editors else []
        moderator_content = self._group_emails_in_lines("* Moderator= ", self._moderators) if self._moderators else []

        content = (
                COMMON_HEADER_CONTENT[:1] +
                ["* " + self._description] +
                COMMON_HEADER_CONTENT[1:] +
                COMMON_CONTENT +
                owner_content +
                editor_content +
                moderator_content +
                self.specific_content()
        )

        if self._has_notebook:
            content += [
                "* Digest= Yes,Same,Monthly",
                f"* Notebook= Yes,{BASE_NOTEBOOK_PATH / list_name},Monthly",
                "* Notebook= Private"
            ]
        else:
            content.append("* Notebook= No")

        content += [subject_tag] + COMMON_FOOTER_CONTENT
        sorted_content = content[:2] + sorted(content[2:-2], key=lambda x: (x[0] != '*', x)) + content[-2:]
        return sorted_content

    def specific_content(self):
        """Contenu spécifique pour cette configuration. À remplacer par des classes dérivées."""
        return []


class ProtoDiffusion(ProtoConfig):
    """Classe représentant une configuration ProtoDiffusion."""

    def specific_content(self):
        return [
            "* Reply-To= Sender,Respect",
            "* Review= Owner",
            "* Send= Owner",
            "* Send= Confirm"
        ]


class ProtoDiffusionArch(ProtoDiffusion):
    """Classe représentant une configuration ProtoDiffusion avec archives."""

    def __init__(self, description, owners):
        super().__init__(description, owners, has_notebook=True)


class ProtoDistr(ProtoConfig):
    """Classe représentant une configuration ProtoDistr."""

    def __init__(self, description, owners):
        super().__init__(description, owners, has_notebook=True)

    def specific_content(self):
        return [
            "* Reply-To= List,Respect",
            "* Review= Private",
            "* Send= Private"
        ]


class ProtoModr(ProtoDiffusion):
    """Classe représentant une configuration ProtoModr."""

    def __init__(self, description, owners, editors, moderators):
        super().__init__(description, owners, has_notebook=True)
        self._editors = editors
        self._moderators = moderators

    def specific_content(self):
        return [
            "* Default-Options= Review",
            "* Reply-To= List,Respect",
            "* Review= Private",
            "* Send= Editor,Hold,Confirm"
        ]


import json


# from proto_config import ProtoDiffusion, ProtoDiffusionArch, ProtoDistr, ProtoModr
# from list_file_writer import ListFileWriter


def read_list_configuration(file_path="configuration_liste.json"):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data


def main():
    config_data = read_list_configuration()

    # Extracting necessary data from config_data
    type_liste = config_data.get("type_liste").lower()
    if type_liste not in [e.value for e in ListType]:
        print(f"Error: tipo de lista no válido. Debe ser uno de: {', '.join([e.value for e in ListType])}")
        exit(1)
    filename = config_data.get("nom_fichier").strip().lower().replace(" ", "-")
    description = config_data.get("description")
    proprietaires = config_data.get("proprietaires")
    editeurs = config_data.get("editeurs", [])
    moderateurs = config_data.get("moderateurs", [])

    # Mapping the type_liste to the correct class
    list_mapping = {
        "proto-std": ProtoDiffusion,
        "proto-std-arch": ProtoDiffusionArch,
        "proto-distr": ProtoDistr,
        "proto-modr": ProtoModr
    }

    list_cls = list_mapping.get(type_liste)

    # Creating list object
    if list_cls == ProtoModr:
        list_obj = list_cls(description, proprietaires, editeurs, moderateurs)
    else:
        list_obj = list_cls(description, proprietaires)

    # Generating content and saving
    content = list_obj.generate_content(filename)
    ListFileWriter.save(filename, content)


if __name__ == "__main__":
    main()