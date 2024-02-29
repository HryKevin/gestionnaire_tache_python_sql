# Importation des modules nécessaires pour la connexion à la base de données MySQL
import mysql.connector
from mysql.connector import Error

# Fonction pour établir la connexion à la base de données
def connect_to_database():
    try:
        # Tentative de connexion à la base de données MySQL avec les informations d'identification
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Remplacez par votre mot de passe MySQL
            database="Pydo"
        )
        # Vérification de la connexion réussie
        if connection.is_connected():
            print("Connecté à la base de données.")
            return connection
    except Error as e:
        # Gestion des erreurs de connexion et affichage du message d'erreur
        print(f"Erreur de connexion à la base de données: {e}")
        return None

# Fonction pour afficher les tâches en fonction de l'état spécifié
def afficher_taches(conn, etat_id):
    # Création d'un objet curseur pour exécuter des requêtes SQL
    cursor = conn.cursor()
    # Exécution de la requête SQL SELECT pour récupérer les tâches avec l'ID d'état spécifié
    cursor.execute(f"SELECT * FROM tache WHERE id_etat = {etat_id}")
    # Récupération de toutes les lignes résultantes
    result = cursor.fetchall()

    # Affichage des tâches s'il y en a, sinon indiquer qu'il n'y a aucune tâche
    if result:
        print(f"\nListe des tâches :")
        for row in result:
            print(f"{row[0]}. {row[1]} - {row[2]}")
    else:
        print(f"Aucune tâche dans cet état.")

# Fonction pour ajouter une nouvelle tâche à la base de données
def ajouter_tache(conn, libelle, date_fixee, etat_id):
    cursor = conn.cursor()
    # Exécution de la requête SQL INSERT pour ajouter une nouvelle tâche
    cursor.execute("INSERT INTO tache (libelle, date_fixee, id_etat) VALUES (%s, %s, %s)",
                   (libelle, date_fixee, etat_id))
    # Validation des modifications dans la base de données
    conn.commit()
    print("Tâche ajoutée avec succès!")

# Fonction pour démarrer une tâche en mettant à jour son état dans la base de données
def demarrer_tache(conn, id_tache):
    cursor = conn.cursor()
    # Exécution de la requête SQL UPDATE pour changer l'état de la tâche à "En cours"
    cursor.execute(
        "UPDATE tache SET id_etat = 2 WHERE id_tache = %s", (id_tache,))
    # Validation des modifications dans la base de données
    conn.commit()
    print("Tâche démarrée avec succès!")

# Fonction pour finaliser une tâche en mettant à jour son état dans la base de données
def finaliser_tache(conn, id_tache):
    cursor = conn.cursor()
    # Exécution de la requête SQL UPDATE pour changer l'état de la tâche à "Terminée"
    cursor.execute(
        "UPDATE tache SET id_etat = 3 WHERE id_tache = %s", (id_tache,))
    # Validation des modifications dans la base de données
    conn.commit()
    print("Tâche finalisée avec succès!")

# Fonction pour supprimer une tâche de la base de données
def supprimer_tache(conn, id_tache):
    cursor = conn.cursor()
    # Exécution de la requête SQL DELETE pour supprimer la tâche spécifiée
    cursor.execute("DELETE FROM tache WHERE id_tache = %s", (id_tache,))
    # Validation des modifications dans la base de données
    conn.commit()
    print("Tâche supprimée avec succès!")

# Fonction pour modifier les détails d'une tâche dans la base de données
def modifier_tache(conn, id_tache, nouveau_libelle, nouvelle_date_fixee):
    cursor = conn.cursor()
    # Exécution de la requête SQL UPDATE pour modifier le libellé et la date fixée de la tâche
    cursor.execute("UPDATE tache SET libelle = %s, date_fixee = %s WHERE id_tache = %s",
                   (nouveau_libelle, nouvelle_date_fixee, id_tache))
    # Validation des modifications dans la base de données
    conn.commit()
    print("Tâche modifiée avec succès!")

# Fonction pour afficher les états disponibles dans la base de données
def afficher_etats(conn):
    cursor = conn.cursor()
    # Exécution de la requête SQL SELECT pour récupérer tous les états
    cursor.execute("SELECT * FROM etat")
    # Récupération de toutes les lignes résultantes
    result = cursor.fetchall()

    # Affichage des états
    print("\nListe des états :")
    for row in result:
        print(f"{row[0]}. {row[1]}")

    return result

# Fonction pour afficher le menu principal de l'application
def afficher_menu():
    print("\nMenu :")
    print("1. Afficher les tâches à faire")
    print("2. Afficher les tâches en cours")
    print("3. Afficher les tâches terminées")
    print("4. Ajouter une nouvelle tâche")
    print("5. Démarrer une tâche")
    print("6. Finaliser une tâche")
    print("7. Supprimer une tâche")
    print("8. Modifier une tâche")
    print("9. Afficher les états")
    print("10. Quitter")

    # Demande à l'utilisateur de choisir une option du menu
    choix = input("Choisissez une option : ")
    return choix

# Fonction principale de l'application
def main():
    # Établissement de la connexion à la base de données
    connexion = connect_to_database()

    # Vérification si la connexion est réussie
    if connexion:
        # Affichage des états disponibles dans la base de données
        etats = afficher_etats(connexion)

        # Boucle principale de l'application
        while True:
            # Affichage du menu et récupération du choix de l'utilisateur
            choix = afficher_menu()

            # Exécution de l'action correspondante en fonction du choix de l'utilisateur
            if choix == "1":
                afficher_taches(connexion, etats[0][0])

            elif choix == "2":
                afficher_taches(connexion, etats[1][0])

            elif choix == "3":
                afficher_taches(connexion, etats[2][0])

            elif choix == "4":
                libelle = input("Entrez le libellé de la tâche : ")
                date_fixee = input("Entrez la date fixée (YYYY-MM-DD) : ")
                ajouter_tache(connexion, libelle, date_fixee, etats[0][0])

            elif choix == "5":
                id_tache = input("Entrez l'ID de la tâche à démarrer : ")
                demarrer_tache(connexion, id_tache)

            elif choix == "6":
                id_tache = input("Entrez l'ID de la tâche à finaliser : ")
                finaliser_tache(connexion, id_tache)

            elif choix == "7":
                id_tache = input("Entrez l'ID de la tâche à supprimer : ")
                supprimer_tache(connexion, id_tache)

            elif choix == "8":
                id_tache = input("Entrez l'ID de la tâche à modifier : ")
                nouveau_libelle = input("Entrez le nouveau libellé : ")
                nouvelle_date_fixee = input(
                    "Entrez la nouvelle date fixée (YYYY-MM-DD) : ")
                modifier_tache(connexion, id_tache,
                               nouveau_libelle, nouvelle_date_fixee)

            elif choix == "9":
                afficher_etats(connexion)

            elif choix == "10":
                print("Au revoir!")
                break

            else:
                print("Option invalide. Veuillez réessayer.")

        # Fermeture de la connexion à la base de données à la sortie de l'application
        connexion.close()

# Exécution de la fonction principale si le script est exécuté directement
if __name__ == "__main__":
    main()
