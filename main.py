import json
from proto_config import ProtoDiffusion, ProtoDiffusionArch, ProtoDistr, ProtoModr
from list_file_writer import ListFileWriter


def read_list_configuration(file_path="configuracion_lista.json"):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data


def main():
    config_data = read_list_configuration()

    # Extracting necessary data from config_data
    tipo_lista = config_data.get("tipo_lista")
    filename = config_data.get("nombre_archivo")
    descripcion = config_data.get("descripcion")
    propietarios = config_data.get("propietarios")
    editores = config_data.get("editores", [])
    moderadores = config_data.get("moderadores", [])

    # Mapping the tipo_lista to the correct class
    list_mapping = {
        "proto-std": ProtoDiffusion,
        "proto-std-arch": ProtoDiffusionArch,
        "proto-distr": ProtoDistr,
        "proto-modr": ProtoModr
    }

    list_cls = list_mapping.get(tipo_lista)

    # Creating list object
    if list_cls == ProtoModr:
        list_obj = list_cls(descripcion, propietarios, editores, moderadores)
    else:
        list_obj = list_cls(descripcion, propietarios)

    # Generating content and saving
    content = list_obj.generate_content(filename)
    ListFileWriter.save(filename, content)

if __name__ == "__main__":
    main()