class ProtoConfig:
    def __init__(self, subject_tag, owner):
        # Propiedades comunes
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

        # Establecer propiedades de notebook por defecto
        self.notebook_active = "Yes"
        list_name = self.subject_tag.replace('"', '').lower()
        self.notebook_path = f"/home/listserv/lists/archives/{list_name}"
        self.notebook_frequency = "Monthly"

    def write_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write("*\n")
            file.write(f"* {self.subject_tag}\n")
            file.write("*\n")
            file.write("*\n")
            file.write("* .HH ON\n")

            # Escribir propiedades en orden alfabético y respetando el formato de mayúsculas y minúsculas
            for key in sorted(vars(self)):
                if key == "notebook_active":
                    file.write(f'* Notebook= {self.notebook_active},{self.notebook_path},{self.notebook_frequency}\n')
                else:
                    file.write(f'* {key.replace("_", "-").title()}= {vars(self)[key]}\n')

            file.write("* .HH OFF\n")
            file.write("*\n")


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


# Crear instancias y escribir a archivos
proto_distr_instance = ProtoDistr()
proto_std_instance = ProtoStd()
proto_std_arch_instance = ProtoStdArch()
proto_modr_instance = ProtoModr()

proto_distr_instance.write_to_file("proto-distr.txt")
proto_std_instance.write_to_file("proto-std.txt")
proto_std_arch_instance.write_to_file("proto-std-arch.txt")
proto_modr_instance.write_to_file("proto-modr.txt")
