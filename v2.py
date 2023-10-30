from pathlib import Path

# Constants
BASE_NOTEBOOK_PATH = Path("/home/listserv/lists/archives")
MAX_LINE_LENGTH = 80

# Common content for all lists
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


class ProtoConfig:
    def __init__(self, description, owners, has_notebook=False):
        self._description = description
        self._owners = owners
        self._editors = []
        self._moderators = []
        self._has_notebook = has_notebook

    def _group_emails_in_lines(self, label, emails):
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
        raise NotImplementedError("Subclasses should implement this method.")


class ProtoDiffusion(ProtoConfig):
    def specific_content(self):
        return [
            "* Reply-To= Sender,Respect",
            "* Review= Owner",
            "* Send= Owner",
            "* Send= Confirm"
        ]

class ProtoDiffusionArch(ProtoDiffusion):
    def __init__(self, description, owners):
        super().__init__(description, owners, has_notebook=True)
class ProtoDistr(ProtoConfig):
    def __init__(self, description, owners):
        super().__init__(description, owners, has_notebook=True)

    def specific_content(self):
        return [
            "* Reply-To= List,Respect",
            "* Review= Private",
            "* Send= Private"
        ]

class ProtoModr(ProtoDiffusion):
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
class ListFileWriter:
    @staticmethod
    def save(filename, content):
        try:
            with open(filename, 'w') as f:
                f.write('\n'.join(content))
        except Exception as e:
            print(f"Error writing to file {filename}: {e}")


def main():
    lists = {
        "proto-std.txt": ProtoDiffusion,
        "proto-std-arch.txt": ProtoDiffusionArch,
        "proto-distr.txt": ProtoDistr,
        "proto-modr.txt": ProtoModr
    }

    descriptions = {
        "proto-std.txt": "Liste prototype standard",
        "proto-std-arch.txt": "Prototype liste de diffusion avec archives",
        "proto-distr.txt": "Liste prototype de distribution (discussion) avec archives",
        "proto-modr.txt": "Liste prototype avec moderateur"
    }

    for filename, list_cls in lists.items():
        description = descriptions[filename]
        if list_cls == ProtoModr:
            list_obj = list_cls(description,
                                ["owner1@test.com", "owner2@test.com"],
                                ["editor@test.com"],
                                ["moderator@test.com"])
        else:
            list_obj = list_cls(description, ["owner1@test.com", "owner2@test.com"])
        content = list_obj.generate_content(filename)
        ListFileWriter.save(filename, content)

if __name__ == "__main__":
    main()
