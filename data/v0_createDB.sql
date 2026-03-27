PRAGMA foreign_keys=on  ;

-- Table LesParticipants
CREATE TABLE LesParticipants (
    numPar INTEGER NOT NULL,
    CONSTRAINT pk_LesParticipants PRIMARY KEY (numPar)
);

-- Table LesSportifs
CREATE TABLE LesSportifs (
    numSp INTEGER NOT NULL,
    nomSp TEXT NOT NULL,
    prenomSp TEXT NOT NULL,
    pays TEXT NOT NULL,
    categorieSp TEXT NOT NULL,
    dateNaisSp DATE NOT NULL,
    CONSTRAINT pk_LesSportifs PRIMARY KEY (numSp),
    CONSTRAINT fk_LesSportifs_LesParticipants FOREIGN KEY (numSp) REFERENCES LesParticipants(numPar),
    CONSTRAINT ck_LesSportifs_numSp CHECK (numSp>1000 AND numSp<1500),
    CONSTRAINT ck_LesSportifs_categorie CHECK (categorieSp = 'masculin' OR categorieSp = 'feminin' OR categorieSp = 'mixte')
);

-- Table LesEquipes
CREATE TABLE LesEquipes_base (
    numEq INTEGER NOT NULL,
    CONSTRAINT pk_lesequipes PRIMARY KEY (numEq),
    CONSTRAINT fk_lesequipes_LesParticipants FOREIGN KEY (numEq) REFERENCES LesParticipants(numPar),
    CONSTRAINT ck_LesSportifs_numSp CHECK (numEq>0 AND numEq<100)
);

-- Table appartient (association entre LesSportifs et LesEquipes) 
CREATE TABLE LesSportifsEQ (
    numSp INTEGER NOT NULL, 
    numEq INTEGER NOT NULL, 
    CONSTRAINT pk_appartient PRIMARY KEY (numSp, numEq),
    CONSTRAINT fk_appartient_sportif FOREIGN KEY (numSp) REFERENCES LesSportifs(numSp),
    CONSTRAINT fk_appartient_equipe FOREIGN KEY (numEq) REFERENCES LesEquipes_base(numEq)
);

-- Table LesDisciplines
CREATE TABLE LesDisciplines (
    nomDi TEXT NOT NULL,
    CONSTRAINT pk_lesdisciplines PRIMARY KEY (nomDi)
);

-- Table LesEpreuves
CREATE TABLE LesEpreuves (
    numEp INTEGER NOT NULL,
    nomEp TEXT NOT NULL,
    formeEp TEXT NOT NULL,
    categorieEp TEXT NOT NULL,
    nbSportifsEp INTEGER,
    dateEp DATE,
    nomDi TEXT NOT NULL,
    CONSTRAINT pk_lesepreuves PRIMARY KEY (numEp),
    CONSTRAINT fk_lesepreuves_discipline FOREIGN KEY (nomDi) REFERENCES LesDisciplines(nomDi),
    CONSTRAINT ck_lesepreuves_forme CHECK (formeEp = 'par equipe' OR formeEp = 'par couple' OR formeEp = 'individuelle'),
    CONSTRAINT ck_lesepreuves_categorie CHECK (categorieEp = 'masculin' OR categorieEp = 'feminin' OR categorieEp = 'mixte')
);

-- Table LesResultats
CREATE TABLE LesResultats (
    numPar INTEGER NOT NULL,
    numEp INTEGER NOT NULL,
    medaille TEXT,
    CONSTRAINT pk_lesresultats PRIMARY KEY (numPar, numEp),
    CONSTRAINT fk_lesresultats_LesParticipants FOREIGN KEY (numPar) REFERENCES LesParticipants(numPar),
    CONSTRAINT fk_lesresultats_epreuve FOREIGN KEY (numEp) REFERENCES LesEpreuves(numEp),
    CONSTRAINT ck_lesresultats_medaille CHECK (medaille = 'gold' OR medaille = 'bronze' OR medaille = 'silver')
);

-- Table LesInscriptions (association entre LesParticipants et LesEpreuves)
CREATE TABLE LesInscriptions (
    numPar INTEGER NOT NULL,
    numEp INTEGER NOT NULL,
    CONSTRAINT pk_LesInscriptions PRIMARY KEY (numPar, numEp),
    CONSTRAINT fk_LesInscriptions_LesParticipants FOREIGN KEY (numPar) REFERENCES LesParticipants(numPar),
    CONSTRAINT fk_LesInscriptions_epreuve FOREIGN KEY (numEp) REFERENCES LesEpreuves(numEp)
);


CREATE VIEW LesAgesSportifs AS
SELECT 
    numSp, 
    nomSp, 
    prenomSp, 
    pays, 
    categorieSp, 
    dateNaisSp,
    CAST(strftime('%Y', 'now') AS INTEGER) - CAST(strftime('%Y', dateNaisSp) AS INTEGER) AS ageSp
FROM LesSportifs;


CREATE VIEW LesNbsEquipiers AS
SELECT 
    numEq,
    COUNT(numSp) AS nbEquipiersEq
FROM LesSportifsEQ
GROUP BY numEq;



CREATE VIEW AgeMoyenEquipesOr AS
SELECT 
    AVG(ageSp) AS ageMoyen
FROM LesAgesSportifs
WHERE numSp IN (
    SELECT s.numSp
    FROM LesSportifsEQ s
    JOIN LesResultats r ON s.numEq = r.numPar
    WHERE r.medaille = 'gold'
);


CREATE VIEW ClassementPays AS
SELECT 
    s.pays,
    (SELECT COUNT(DISTINCT numEp) FROM (
        SELECT r.numEp FROM LesSportifs s2 JOIN LesResultats r ON s2.numSp = r.numPar 
        WHERE s2.pays = s.pays AND r.medaille = 'gold'
        UNION
        SELECT r.numEp FROM LesSportifs s2 JOIN LesSportifsEQ seq ON s2.numSp = seq.numSp 
        JOIN LesResultats r ON seq.numEq = r.numPar WHERE s2.pays = s.pays AND r.medaille = 'gold'
    )) AS nbOr,
    (SELECT COUNT(DISTINCT numEp) FROM (
        SELECT r.numEp FROM LesSportifs s2 JOIN LesResultats r ON s2.numSp = r.numPar 
        WHERE s2.pays = s.pays AND r.medaille = 'silver'
        UNION 
        SELECT r.numEp FROM LesSportifs s2 JOIN LesSportifsEQ seq ON s2.numSp = seq.numSp 
        JOIN LesResultats r ON seq.numEq = r.numPar WHERE s2.pays = s.pays AND r.medaille = 'silver'
    )) AS nbArgent,
    (SELECT COUNT(DISTINCT numEp) FROM (
        SELECT r.numEp FROM LesSportifs s2 JOIN LesResultats r ON s2.numSp = r.numPar 
        WHERE s2.pays = s.pays AND r.medaille = 'bronze'
        UNION
        SELECT r.numEp FROM LesSportifs s2 JOIN LesSportifsEQ seq ON s2.numSp = seq.numSp 
        JOIN LesResultats r ON seq.numEq = r.numPar WHERE s2.pays = s.pays AND r.medaille = 'bronze'
    )) AS nbBronze
FROM LesSportifs s
GROUP BY s.pays
ORDER BY nbOr DESC, nbArgent DESC, nbBronze DESC;