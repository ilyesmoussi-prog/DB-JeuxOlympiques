import sqlite3
from datetime import datetime, timedelta


def test_trigger_1_age_minimum(data):
    print("\n" + "="*60)
    print("TEST 1 : Âge minimum de 18 ans")
    print("="*60)
    
    cursor = data.cursor()

    try: 
        cursor.execute("SELECT MAX(numSp) FROM LesSportifs WHERE numSp BETWEEN 1000 AND 1499")
        max_num = cursor.fetchone()[0]
        num_majeur = 1400 if max_num is None else max_num + 1
        num_mineur = num_majeur + 1
        
        sql = f"INSERT INTO LesParticipants (numPar) VALUES ({num_majeur})"
        print(f"\n{sql}")
        cursor.execute(sql)
        
        sql = f"INSERT INTO LesParticipants (numPar) VALUES ({num_mineur})"
        print(f"{sql}")
        cursor.execute(sql)
        data.commit()
        
        date_25_ans = (datetime.now() - timedelta(days=25*365)).strftime('%Y-%m-%d')
        sql = f"INSERT INTO LesSportifs (numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp) VALUES ({num_majeur}, 'Majeur', 'Jean', 'France', 'masculin', '{date_25_ans}')"
        print(f"\n{sql}")
        try:
            cursor.execute(sql)
            data.commit()
            print(">>> Insertion réussie - Sportif majeur accepté\n")
        except sqlite3.Error as e:
            print(f" {e}\n")
            data.rollback()
        
        date_16_ans = (datetime.now() - timedelta(days=16*365)).strftime('%Y-%m-%d')
        sql = f"INSERT INTO LesSportifs (numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp) VALUES ({num_mineur}, 'Mineur', 'Pierre', 'France', 'masculin', '{date_16_ans}')"
        print(f"{sql}")
        try:
            cursor.execute(sql)
            data.commit()
            print(">>> ERREUR - Sportif mineur accepté (le trigger n'a pas fonctionné!)\n")
        except sqlite3.Error as e:
            print(f" {e}\n")
            data.rollback()
        
        cursor.close()

    except sqlite3.IntegrityError as e:
        print(f"\n Données de test déjà existantes. Utilisez d'abord l'option 3 puis 1 et 2.\n")
        data.rollback()
    finally:
        cursor.close()


def test_trigger_2_forme_epreuve(data):
    print("\n" + "="*60)
    print("TEST 2 : Cohérence forme épreuve / type participant")
    print("="*60)
    
    cursor = data.cursor()

    sql = "INSERT OR IGNORE INTO LesDisciplines (nomDi) VALUES ('TestDiscipline')"
    print(f"\n{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesParticipants (numPar) VALUES (1102)"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesParticipants (numPar) VALUES (1103)"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesParticipants (numPar) VALUES (50)"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesSportifs (numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp) VALUES (1102, 'Test', 'Individuel', 'France', 'masculin', '1990-01-01')"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesSportifs (numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp) VALUES (1103, 'Test2', 'Solo', 'France', 'masculin', '1990-01-01')"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesEquipes_base (numEq) VALUES (50)"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesEpreuves (numEp, nomEp, formeEp, categorieEp, nbSportifsEp, dateEp, nomDi) VALUES (5001, 'Test 100m', 'individuelle', 'masculin', 8, '2024-08-01', 'TestDiscipline')"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesEpreuves (numEp, nomEp, formeEp, categorieEp, nbSportifsEp, dateEp, nomDi) VALUES (5002, 'Test Relais', 'par equipe', 'masculin', 4, '2024-08-02', 'TestDiscipline')"
    print(f"{sql}")
    cursor.execute(sql)
    data.commit()
    
    sql = "INSERT INTO LesInscriptions (numPar, numEp) VALUES (1102, 5001)"
    print(f"\n{sql}")
    try:
        cursor.execute(sql)
        data.commit()
        print(">>> Sportif : épreuve individuelle accepté\n")
    except sqlite3.Error as e:
        print(f" {e}\n")
        data.rollback()
    
    sql = "INSERT INTO LesInscriptions (numPar, numEp) VALUES (50, 5001)"
    print(f"{sql}")
    try:
        cursor.execute(sql)
        data.commit()
        print(">>> ERREUR - Équipe acceptée pour épreuve individuelle!\n")
    except sqlite3.Error as e:
        print(f" {e}\n")
        data.rollback()
    
    sql = "INSERT INTO LesInscriptions (numPar, numEp) VALUES (1103, 5002)"
    print(f"{sql}")
    try:
        cursor.execute(sql)
        data.commit()
        print(">>> ERREUR - Sportif accepté pour épreuve par équipe!\n")
    except sqlite3.Error as e:
        print(f" {e}\n")
        data.rollback()
    
    cursor.close()



def test_trigger_3_doublon_medaille(data):
    print("\n" + "="*60)
    print("TEST 3 : Interdiction doublons médailles")
    print("="*60)
    
    cursor = data.cursor()
    
    
    sql = "INSERT OR IGNORE INTO LesParticipants (numPar) VALUES (1104)"
    print(f"\n{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesSportifs (numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp) VALUES (1104, 'Champion', 'Marie', 'France', 'feminin', '1995-05-15')"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesDisciplines (nomDi) VALUES ('TestDiscipline')"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesEpreuves (numEp, nomEp, formeEp, categorieEp, nbSportifsEp, dateEp, nomDi) VALUES (5003, 'Test Natation', 'individuelle', 'feminin', 8, '2024-08-01', 'TestDiscipline')"
    print(f"{sql}")
    cursor.execute(sql)
    
    sql = "INSERT OR IGNORE INTO LesInscriptions (numPar, numEp) VALUES (1104, 5003)"
    print(f"{sql}")
    cursor.execute(sql)
    data.commit()
    
    sql = "INSERT INTO LesResultats (numPar, numEp, medaille) VALUES (1104, 5003, 'gold')"
    print(f"\n{sql}")
    try:
        cursor.execute(sql)
        data.commit()
        print(">>> Première médaille attribuée\n")
    except sqlite3.Error as e:
        print(f"{e}\n")
        data.rollback()
    
    sql = "INSERT INTO LesResultats (numPar, numEp, medaille) VALUES (1104, 5003, 'silver')"
    print(f"{sql}")
    try:
        cursor.execute(sql)
        data.commit()
        print(">>> ERREUR - Doublon de médaille accepté!\n")
    except sqlite3.Error as e:
        print(f" {e}\n")
        data.rollback()
    
    cursor.close()
    

def lancer_tous_les_tests(data):
    print("\n" + "="*60)
    print("TESTS DES TRIGGERS")
    print("="*60)
    
    test_trigger_1_age_minimum(data)
    test_trigger_2_forme_epreuve(data)
    test_trigger_3_doublon_medaille(data)

    print("\n" + "="*60)
    print("TESTS TERMINÉS")
    print("="*60)