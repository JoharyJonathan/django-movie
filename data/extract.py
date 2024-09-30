import pandas as pd

# Remplace 'file.csv' par le chemin de ton fichier CSV
df = pd.read_csv('netflix_titles.csv')

# Remplace 'nom_de_la_colonne' par le nom de la colonne que tu veux extraire
colonne = df['cast']

# Écriture des éléments de la colonne dans un fichier TXT avec encodage utf-8
with open('actors.txt', 'w', encoding='utf-8') as f:
    for item in colonne:
        f.write(f"{item}\n")