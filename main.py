import sqlite3
from actions import database_functions
from actions import database_queries
from actions import test_triggers

# Connexion à la base de données
data = sqlite3.connect("data/jo.db")

# Fonction permettant de quitter le programme
def quitter():
    print("Au revoir !")
    exit(0)

# Association des actions aux fonctions
actions = {
    "1": lambda: database_functions.database_create(data),
    "2": lambda: database_functions.database_insert(data),
    "3": lambda: database_functions.database_delete(data),
    "4": lambda: database_queries.liste_epreuves(data, "Ski alpin"),
    "5": lambda: test_triggers.lancer_tous_les_tests(data),
    "6": lambda: test_triggers.test_trigger_1_age_minimum(data),
    "7": lambda: test_triggers.test_trigger_2_forme_epreuve(data),
    "8": lambda: test_triggers.test_trigger_3_doublon_medaille(data),
    "q": quitter
}

# Fonctions d'affichage du menu
def menu():
    print("\n=== Menu principal ===")
    print("1 - Créer la base de données")
    print("2 - Insérer les données du fichier Excel")
    print("3 - Supprimer la base de données")
    print("4 - Liste des épreuves de ski alpin")
    print("\n--- Tests des Triggers ---") 
    print("5 - Lancer TOUS les tests des triggers")
    print("6 - Test Trigger 1 : Âge minimum (18 ans)")
    print("7 - Test Trigger 2 : Cohérence forme épreuve")
    print("8 - Test Trigger 3 : Pas de doublon médaille")
    print("\nq - Quitter")

# Fonction principale
def main():
    # Appel du menu en boucle et gestion du choix
    while True:
        menu()
        choix = input("Votre choix : ").strip()
        action = actions.get(choix)
        if action:
            action()
        else:
            print("Choix invalide.")

# Appel de la fonction principale
main()