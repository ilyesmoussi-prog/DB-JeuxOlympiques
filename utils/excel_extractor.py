import sqlite3, pandas
from sqlite3 import IntegrityError

# Fonction permettant de lire le fichier Excel des JO et d'insérer les données dans la base
def read_excel_file_V0(data:sqlite3.Connection, file):
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    
    # Insertion dans LesParticipants
    numPar_set = set()
    for ix, row in df_sportifs.iterrows():
        numPar_set.add(row['numSp'])
        if row['numEq'] != 'null': 
            numPar_set.add(row['numEq'])
    
    for numPar in numPar_set:
        try:
            query = "insert into LesParticipants values ({})".format(numPar)
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)
    
    # Insertion dans LesSportifs
    sportifs_inseres = set()
    for ix, row in df_sportifs.iterrows():
        try:
            if row['numSp'] not in sportifs_inseres:
                query = "insert into LesSportifs values ({},'{}','{}','{}','{}','{}')".format(
                    row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'])
                print(query)
                cursor.execute(query)
                sportifs_inseres.add(row['numSp'])
        except IntegrityError as err:
            print(err)
    
    # Insertion dans LesEquipes
    equipes_set = set()
    for ix, row in df_sportifs.iterrows():
        if row['numEq'] != 'null':
            equipes_set.add(row['numEq'])

    for numEq in equipes_set:
        try:
            query = "insert into LesEquipes_base values ({})".format(numEq)
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)
    # Insertion dans LesSportifsEQ
    for ix, row in df_sportifs.iterrows():
        try:
            if row['numEq'] != 'null':
                query = "insert into LesSportifsEQ values ({},{})".format(row['numSp'], row['numEq'])
                print(query)
                cursor.execute(query)
        except IntegrityError as err:
            print(err)

    #  lecture dand LesEpreuves 
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    
    # Insertion dans LesDisciplines 
    disciplines_inserees = set()
    for ix, row in df_epreuves.iterrows():
        try:
            if row['nomDi'] not in disciplines_inserees:
                query = "insert into LesDisciplines values ('{}')".format(row['nomDi'])
                print(query)
                cursor.execute(query)
                disciplines_inserees.add(row['nomDi'])
        except IntegrityError as err:
            print(err)
    
    # Insertion dans LesEpreuves
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert into LesEpreuves values ({},'{}','{}','{}',{},".format(
                row['numEp'], row['nomEp'], row['formeEp'], row['categorieEp'], row['nbSportifsEp'])

            if row['dateEp'] != 'null':
                query = query + "'{}','{}')".format(row['dateEp'], row['nomDi'])
            else:
                query = query + "null,'{}')".format(row['nomDi'])
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    df_inscriptions = pandas.read_excel(file, sheet_name='LesInscriptions', dtype=str)
    df_inscriptions = df_inscriptions.where(pandas.notnull(df_inscriptions), 'null')
    
    for ix, row in df_inscriptions.iterrows():
        try:
            # numIn < 100 = équipe, sinon = sportif
            numPar = row['numIn']
            numEp = row['numEp']
            query = "insert into LesInscriptions values ({},{})".format(numPar, numEp)
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)
    
    # Lecture dans LesResultats
    df_resultats = pandas.read_excel(file, sheet_name='LesResultats', dtype=str)
    df_resultats = df_resultats.where(pandas.notnull(df_resultats), 'null')
    
    for ix, row in df_resultats.iterrows():
        try:
            numEp = row['numEp']
            if row['gold'] != 'null':
                numPar = row['gold']
                medaille = 'gold'
                query = "insert into LesResultats values ({},{},'{}')".format(numPar, numEp, medaille)
                print(query)
                cursor.execute(query)
            if row['silver'] != 'null':
                numPar = row['silver']
                medaille = 'silver'
                query = "insert into LesResultats values ({},{},'{}')".format(numPar, numEp, medaille)
                print(query)
                cursor.execute(query)
            if row['bronze'] != 'null':
                numPar = row['bronze']
                medaille = 'bronze'
                query = "insert into LesResultats values ({},{},'{}')".format(numPar, numEp, medaille)
                print(query)
                cursor.execute(query)
        except IntegrityError as err:
            print(err)