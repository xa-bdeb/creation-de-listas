class ListConfig:
    MAX_LINE_LENGTH = 80
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

    @staticmethod
    def get_common_header(description: str):
        return ListConfig.COMMON_HEADER_CONTENT[:1] + [f"* {description}"] + ListConfig.COMMON_HEADER_CONTENT[1:]

    @staticmethod
    def get_common_content():
        return ListConfig.COMMON_CONTENT

    @staticmethod
    def get_common_footer():
        return ListConfig.COMMON_FOOTER_CONTENT


class BaseList:
    def __init__(self, description, owners, editors=None, moderators=None):
        self._description = description
        self._owners = owners
        self._editors = editors or []
        self._moderators = moderators or []

    def _format_emails(self, label, emails):
        return [f"{label} {', '.join(emails)}"]

    def generate_content(self, filename):
        list_name_upper = filename.replace(".txt", "").upper()
        subject_tag = f'* Subject-Tag= "{list_name_upper}"'
        owner_content = self._format_emails("* Owner=", self._owners)
        editor_content = self._format_emails("* Editor=", self._editors) if self._editors else []
        moderator_content = self._format_emails("* Moderator=", self._moderators) if self._moderators else []

        content = (
                ListConfig.get_common_header(self._description) +
                ListConfig.get_common_content() +
                owner_content +
                editor_content +
                moderator_content +
                self.specific_content(list_name_upper) +
                ["* Notebook= No", subject_tag] +
                ListConfig.get_common_footer()
        )

        seen = set()
        content = [x for x in content if not (x in seen or seen.add(x))]
        sorted_content = content[:2] + sorted(content[2:-2], key=lambda x: (x[0] != '*', x)) + content[-2:]

        return sorted_content

    def specific_content(self, list_name_upper):
        return []


class DiffusionList(BaseList):
    pass


class DistributionList(BaseList):
    def specific_content(self, list_name_upper):
        return [
            "* Reply-To= List,Respect",
            "* Review= Private",
            "* Send= Private",
            "* Digest= Yes,Same,Monthly",
            f"* Notebook= Yes,/home/listserv/lists/archives/{list_name_upper},Monthly",
            "* Notebook= Private"
        ]


class DistributionWithArchiveList(DistributionList):
    pass


class DistributionWithModeratorList(DistributionWithArchiveList):
    def specific_content(self, list_name_upper):
        base_content = super().specific_content(list_name_upper)
        additional_content = {
            "* Reply-To=": "* Reply-To= List,Respect",
            "* Review=": "* Review= Private",
            "* Send=": "* Send= Editor,Hold,Confirm"
        }

        for index, line in enumerate(base_content):
            key = line.split(' ')[0]
            if key in additional_content:
                base_content[index] = additional_content[key]

        return base_content


def save_to_file(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write('\n'.join(content))
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")


def main():
    lists = {
        "proto-std.txt": (DiffusionList, "Liste prototype standard"),
        "proto-std-arch.txt": (DistributionWithArchiveList, "Prototype liste de diffusion avec archives"),
        "proto-distr.txt": (DistributionList, "Liste prototype de distribution (discussion) avec archives"),
        "proto-modr.txt": (DistributionWithModeratorList, "Liste prototype avec moderateur")
    }

    for filename, (list_cls, description) in lists.items():
        args = [description, ["owner1@test.com", "owner2@test.com"]]

        if list_cls == DistributionWithModeratorList:
            args.extend([["editor@test.com"], ["moderator@test.com"]])

        list_obj = list_cls(*args)
        content = list_obj.generate_content(filename)
        save_to_file(filename, content)


if __name__ == "__main__":
    main()
