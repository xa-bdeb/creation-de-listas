from pathlib import Path

# Constants
BASE_NOTEBOOK_PATH = Path("/home/listserv/lists/archives")
MAX_LINE_LENGTH = 80
class ProtoConfig:
    def __init__(self, subject_tag, owner):
        # Common properties
        self.misc_options = "UTF8_HEADER"
        self.change_log = "Yes"
        self.attachments = "Yes"
        self.service = "*"
        self.errors_to = "Owners"
        self.loopcheck = "NoSpam"
        self.validate = "No"
        self.language = "FRANCAIS"
        self.subscription = "By_Owner"
        self.sender = "None"
        self.auto_delete = "Yes,Semi-Auto,Delay(4),Max(6),Probe(30)"
        self.ack = "Yes"
        self.notify = "Yes"
        self.confidential = "Yes"
        self.subject_tag = subject_tag
        self.owner = owner

    def write_to_file(self, filename, description_line):
        with open(filename, 'w') as file:
            # Writing the header
            file.write(generate_header(description_line))
            file.write("* .HH ON\n")
            for key in sorted(vars(self)):
                    file.write(f'* {key.replace("_", "-").title()}= {vars(self)[key]}\n')
            file.write("* .HH OFF\n")
            file.write("*\n")

def generate_header(description_line):
    return f"*\n* {description_line}\n*\n*\n"

class ProtoDistr(ProtoConfig):
    def __init__(self):
        super().__init__(subject_tag='"PROTO-DISTR"', owner="owner1@test.com,owner2@test.com")
        self.send = "Private"
        self.reply_to = "List,Respect"
        self.review = "Private"

class ProtoStd(ProtoConfig):
    def __init__(self):
        super().__init__(subject_tag='"PROTO-STD"', owner="owner1@test.com,owner2@test.com")
        self.send = "Owner"
        self.reply_to = "Sender,Respect"
        self.review = "Owner"

class ProtoStdArch(ProtoConfig):
    def __init__(self):
        super().__init__(subject_tag='"PROTO-STD-ARCH"', owner="owner1@test.com, owner2@test.com")
        self.send = "Confirm"
        self.reply_to = "Sender,Respect"
        self.review = "Owner"

class ProtoModr(ProtoConfig):
    def __init__(self):
        super().__init__(subject_tag='"PROTO-MODR"', owner="owner1@test.com,owner2@test.com")
        self.send = "Editor,Hold,Confirm"
        self.reply_to = "List,Respect"
        self.review = "Private"

# Create instances and write to files
proto_distr_instance = ProtoDistr()
proto_std_instance = ProtoStd()
proto_std_arch_instance = ProtoStdArch()
proto_modr_instance = ProtoModr()

proto_distr_instance.write_to_file("proto-distr.txt", "Liste prototype de distribution (discussion) avec archives")
proto_std_instance.write_to_file("proto-std.txt", "Liste prototype standard")
proto_std_arch_instance.write_to_file("proto-std-arch.txt", "Prototype liste de diffusion avec archives")
proto_modr_instance.write_to_file("proto-modr.txt", "Liste prototype avec moderateur")
