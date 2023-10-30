from constants import MAX_LINE_LENGTH, COMMON_HEADER_CONTENT, COMMON_CONTENT, COMMON_FOOTER_CONTENT, BASE_NOTEBOOK_PATH
from pathlib import Path


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
