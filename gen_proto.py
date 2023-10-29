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
        self.notebook_active = None
        self.notebook_path = None
        self.notebook_frequency = None

    def set_notebook(self, active, path=None, frequency=None):
        self.notebook_active = active
        self.notebook_path = path
        self.notebook_frequency = frequency

    def get_notebook(self):
        if self.notebook_active == "Yes":
            return f"{self.notebook_active},{self.notebook_path},{self.notebook_frequency}"
        return self.notebook_active

    def write_to_file(self, filename):
        with open(filename, 'w') as file:
            # Escribir el encabezado
            file.write("*\n")
            file.write("* Lista prototipo de {}\n".format(self.subject_tag.replace('"', '')))
            file.write("*\n")
            file.write("*\n")
            file.write("* .HH ON\n")

            # Escribir propiedades en orden alfabético y respetando el formato de mayúsculas y minúsculas
            for key in sorted(vars(self)):
                # Para la propiedad "notebook", usamos el método get_notebook
                if key == "notebook_active":
                    file.write(f'* Notebook= {self.get_notebook()}\n')
                else:
                    file.write(f'* {key.replace("_", "-").title()}= {vars(self)[key]}\n')

            # Escribir el pie de página
            file.write("* .HH OFF\n")
            file.write("*\n")


class ProtoDistr(ProtoConfig):
    def __init__(self):
        super().__init__(subject_tag='"PROTO-DISTR"', owner="owner1@test.com,owner2@test.com")
        self.send = "Private"
        self.reply_to = "List,Respect"
        self.review = "Private"
        self.set_notebook("Yes", "/home/listserv/lists/archives/proto-distr", "Monthly")


class ProtoStd(ProtoConfig):
    def __init__(self):
        super().__init__(subject_tag='"PROTO-STD"', owner="owner1@test.com,owner2@test.com")
        self.send = "Owner"
        self.reply_to = "Sender,Respect"
        self.review = "Owner"
        self.notebook_active = "No"


class ProtoStdArch(ProtoConfig):
    def __init__(self):
        super().__init__(subject_tag='"PROTO-STD-ARCH"', owner="owner1@test.com, owner2@test.com")
        self.send = "Confirm"
        self.reply_to = "Sender,Respect"
        self.review = "Owner"
        self.set_notebook("Yes", "/home/listserv/lists/archives/proto-std-arch", "Monthly")


class ProtoModr(ProtoConfig):
    def __init__(self):
        super().__init__(subject_tag='"PROTO-MODR"', owner="owner1@test.com,owner2@test.com")
        self.send = "Editor,Hold,Confirm"
        self.reply_to = "List,Respect"
        self.review = "Private"
        self.set_notebook("Yes", "/home/listserv/lists/archives/proto-modr", "Monthly")


# Crear instancias y escribir a archivos
proto_distr_instance = ProtoDistr()
proto_std_instance = ProtoStd()
proto_std_arch_instance = ProtoStdArch()
proto_modr_instance = ProtoModr()

proto_distr_instance.write_to_file("proto-distr.txt")
proto_std_instance.write_to_file("proto-std.txt")
proto_std_arch_instance.write_to_file("proto-std-arch.txt")
proto_modr_instance.write_to_file("proto-modr.txt")