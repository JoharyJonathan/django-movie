import random
from datetime import datetime

# Fonction pour générer des entrées fictives
def generate_fake_data(num_entries=100):
    # Ouvrir un fichier SQL pour écrire les données
    with open("fake_user_interactions.sql", "w") as f:
        # Écrire les requêtes SQL
        f.write("BEGIN;\n")
        for i in range(num_entries):
            watched = 'TRUE'  # Always TRUE for SQL boolean
            liked = 'TRUE' if random.choice([True, False]) else 'FALSE'  # TRUE or FALSE
            timestamp = datetime.now().isoformat()  # Current timestamp
            movie_id = random.randint(1, 80)  # Random movie_id between 1 and 80
            user_id = random.randint(1, 20)  # Random user_id between 1 and 20

            # Créer la requête d'insertion SQL pour la table recommendations_usermovieinteraction
            sql = f"INSERT INTO recommendations_usermovieinteraction (watched, liked, timestamp, movie_id, user_id) VALUES ({watched}, {liked}, '{timestamp}', {movie_id}, {user_id});\n"
            f.write(sql)
        f.write("COMMIT;\n")

# Appel de la fonction pour générer et sauvegarder les données
generate_fake_data(100)

print("Les données fictives ont été générées avec succès dans 'fake_user_interactions.sql'.")