# Manuel d'Utilisation du Script de Configuration de Listes d'Envoi

Ce script permet de configurer et de créer différents types de listes d'envoi. Il prend en charge deux types principaux de listes : les listes de diffusion et les listes de distribution.

## Configuration du fichier JSON
Le fichier `configuration_liste.json` contient les paramètres nécessaires pour créer une liste d'envoi. Voici une description de chaque champ :

- **type_liste** : Type de liste à créer.
  - `proto-std` : Liste de diffusion standard, sans archives.
  - `proto-std-arch` : Liste de diffusion standard, avec archives.
  - `proto-distr` : Liste de distribution, avec archives.
  - `proto-modr` : Liste de distribution, avec archives et modérateur.

- **nom_fichier** : Nom du fichier de sortie. **Attention** : Le nom doit être en minuscule (par exemple, 'ABC-123' ne fonctionnera pas).

- **description** : Description de la liste.

- **proprietaires** : Adresses e-mail des propriétaires de la liste.

- **editeurs** : (Optionnel) Adresses e-mail des éditeurs.

- **moderateurs** : (Optionnel) Adresses e-mail des modérateurs.

## Utilisation

1. Sélectionnez le type de liste et utilisez le prototype correspondant.
2. Éditez le fichier `configuration_liste.json` avec les informations requises.
3. Exécutez le script pour obtenir la configuration.

## Notes

Veillez à suivre attentivement les instructions pour garantir le bon fonctionnement du script et la création correcte de la liste d'envoi.

