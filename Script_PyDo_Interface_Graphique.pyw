import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, simpledialog, scrolledtext


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Remplacez par votre mot de passe MySQL
            database="pydo"
        )
        if connection.is_connected():
            print("Connecté à la base de données.")
            return connection
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None


def afficher_taches(conn, text_widget):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_tache, tache.libelle, etat.libelle, tache.id_etat, tache.date_creation, tache.date_fixee, tache.date_realisation FROM tache INNER JOIN etat ON tache.id_etat = etat.id_etat")
    result = cursor.fetchall()

    if result:
        text_widget.insert(tk.END, "Liste des tâches :\n")
        for row in result:
            id_tache = row[0]
            libelle = row[1]
            etat_libelle = row[2]
            etat_id = row[3]
            date_creation = row[4]
            date_fixee = row[5]
            date_realisation = row[6]

            # Ajouter une balise avec la couleur appropriée
            if etat_id == 1:
                tag_name = f"etat_{etat_id}"
                text_widget.tag_configure(tag_name, background='red')
            elif etat_id == 2:
                tag_name = f"etat_{etat_id}"
                text_widget.tag_configure(tag_name, background='orange')
            elif etat_id == 3:
                tag_name = f"etat_{etat_id}"
                text_widget.tag_configure(tag_name, background='green')

            # Insérer la ligne avec la balise appliquée
            text_widget.insert(
                tk.END, f"{id_tache}. {libelle} - État: {etat_libelle} - Date de création: {date_creation} - Date butoir : {date_fixee} - Date de réalisation: {date_realisation}\n", tag_name)
    else:
        text_widget.insert(tk.END, "Aucune tâche.\n")


def modifier_tache(conn, id_tache, nouveau_libelle, nouvelle_date_fixee, nouvelle_date_realisation):
    cursor = conn.cursor()
    cursor.execute("UPDATE tache SET libelle = %s, date_fixee = %s, date_realisation = %s WHERE id_tache = %s",
                   (nouveau_libelle, nouvelle_date_fixee, nouvelle_date_realisation, id_tache))
    conn.commit()
    print("Tâche modifiée avec succès!")


def modifier_etat(conn, id_tache, nouvel_etat):
    cursor = conn.cursor()
    cursor.execute("UPDATE tache SET id_etat = %s WHERE id_tache = %s",
                   (nouvel_etat, id_tache))
    conn.commit()
    print("État de la tâche modifié avec succès!")


def ajouter_tache(conn, libelle, date_fixee):
    cursor = conn.cursor()

    # Récupérer l'ID de l'état "À faire" (à ajuster selon votre structure de données)
    cursor.execute("SELECT id_etat FROM etat WHERE libelle = 'À faire'")
    etat_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO tache (libelle, date_creation, date_fixee, id_etat) VALUES (%s, NOW(), %s, %s)",
                   (libelle, date_fixee, etat_id))
    conn.commit()
    print("Tâche ajoutée avec succès!")


def supprimer_tache(conn, id_tache):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tache WHERE id_tache = %s", (id_tache,))
    conn.commit()
    print("Tâche supprimée avec succès!")


def afficher_etats(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM etat")
    result = cursor.fetchall()

    text = "\nListe des états :\n"
    for row in result:
        text += f"{row[0]}. {row[1]}\n"

    return result, text


class PydoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pydo - Gestionnaire de tâches")
        self.connexion = connect_to_database()
        self.etats = afficher_etats(self.connexion)
        self.initialize_ui()

    def initialize_ui(self):
        ttk.Label(self.master, text="Pydo - Gestionnaire de tâches",
                  font=("Helvetica", 16)).pack(pady=10)

        # Ajout d'une zone de texte pour afficher les résultats
        self.text_widget = scrolledtext.ScrolledText(
            self.master, wrap=tk.WORD, width=80, height=20)
        self.text_widget.pack(pady=10)

        ttk.Button(self.master, text="Afficher toutes les tâches", command=self.afficher_toutes_taches).pack(
            pady=5, padx=5, anchor="center")
        ttk.Button(self.master, text="Modifier l'état d'une tâche", command=self.modifier_etat_tache).pack(
            pady=5, padx=5, anchor="center")
        ttk.Button(self.master, text="Modifier une tâche", command=self.modifier_tache).pack(
            pady=5, padx=5, anchor="center")
        ttk.Button(self.master, text="Ajouter une tâche", command=self.ajouter_tache).pack(
            pady=5, padx=5, anchor="center")
        ttk.Button(self.master, text="Supprimer une tâche", command=self.supprimer_tache).pack(
            pady=5, padx=5, anchor="center")
        ttk.Button(self.master, text="Afficher les états", command=self.afficher_etats).pack(
            pady=5, padx=5, anchor="center")
        ttk.Button(self.master, text="Quitter", command=self.quitter).pack(
            pady=5, padx=5, anchor="center")

    def afficher_toutes_taches(self):
        self.text_widget.delete(1.0, tk.END)  # Efface le contenu précédent
        afficher_taches(self.connexion, self.text_widget)
        self.mettre_a_jour_couleurs_taches()

    def mettre_a_jour_couleurs_taches(self):
        cursor = self.connexion.cursor()
        cursor.execute("SELECT id_tache, id_etat FROM tache")
        result = cursor.fetchall()

        for row in result:
            id_tache = row[0]
            id_etat = row[1]
            tag_name = f"{id_tache}_{id_etat}"

        # Supprimer d'abord la balise existante si elle existe
        self.text_widget.tag_delete(tag_name)

        # Ajouter la nouvelle balise avec la couleur appropriée
        if id_etat == 1:
            self.text_widget.tag_configure(tag_name, background='red')
        elif id_etat == 2:
            self.text_widget.tag_configure(tag_name, background='orange')
        elif id_etat == 3:
            self.text_widget.tag_configure(tag_name, background='green')

        # Appliquer la balise à toute la ligne de la tâche
        self.text_widget.tag_add(tag_name, f"{id_tache}.0", f"{id_tache}.end")

    def modifier_etat_tache(self):
        id_tache = simpledialog.askinteger(
            "Modifier l'état d'une tâche", "Entrez l'ID de la tâche à modifier :")
        nouvel_etat = simpledialog.askinteger(
            "Nouvel état", "Entrez le nouvel état (1 pour À faire, 2 pour En cours, 3 pour Terminée) :")

        if nouvel_etat in {1, 2, 3}:
            modifier_etat(self.connexion, id_tache, nouvel_etat)
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(
                tk.END, "État de la tâche modifié avec succès!\n")
        else:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(
                tk.END, "Erreur : État invalide. Veuillez entrer 1, 2 ou 3.\n")

    def modifier_tache(self):
        id_tache = simpledialog.askinteger(
            "Modifier une tâche", "Entrez l'ID de la tâche à modifier :")
        nouveau_libelle = simpledialog.askstring(
            "Nouveau libellé", "Entrez le nouveau libellé :")
        nouvelle_date_fixee = simpledialog.askstring(
            "Nouvelle date fixée", "Entrez la nouvelle date fixée (YYYY-MM-DD) :")
        nouvelle_date_realisation = simpledialog.askstring(
            "Nouvelle date de réalisation", "Entrez la nouvelle date de réalisation (YYYY-MM-DD) :")

        modifier_tache(self.connexion, id_tache,
                       nouveau_libelle, nouvelle_date_fixee, nouvelle_date_realisation)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, "Tâche modifiée avec succès!\n")

    def ajouter_tache(self):
        libelle = simpledialog.askstring(
            "Libellé", "Entrez le libellé de la tâche :")
        date_fixee = simpledialog.askstring(
            "Date fixée", "Entrez la date fixée (YYYY-MM-DD) :")
    # Nouvelles tâches sont ajoutées avec l'état "A faire"
        ajouter_tache(self.connexion, libelle, date_fixee)

    def supprimer_tache(self):
        id_tache = simpledialog.askinteger(
            "Supprimer une tâche", "Entrez l'ID de la tâche à supprimer :")
        supprimer_tache(self.connexion, id_tache)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, "Tâche supprimée avec succès!\n")

    def afficher_etats(self):
        _, etats_text = afficher_etats(self.connexion)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, etats_text)

    def quitter(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PydoApp(root)
    root.mainloop()
