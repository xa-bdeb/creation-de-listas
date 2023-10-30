class ListFileWriter:
    """Classe pour écrire le contenu de la liste dans un fichier."""
    
    @staticmethod
    def save(filename, content):
        try:
            with open(filename, 'w') as f:
                f.write('\n'.join(content))
        except Exception as e:
            print(f"Erreur lors de l'écriture dans le fichier {filename}: {e}")
