
## TELLAB Belaid
## MOUSSI Ilyes

--- 
# 1- Conception UML et Normalisation


## Question 1 – Dépendances fonctionnelles et normalisation

## 1. Relation LesEpreuves

La relation **_LesEpreuves(numEp, nomEp, formeEp, categorieEp, nbSportifsEp, dateEp, nomDi)_** représente les épreuves d’une discipline.  
Chaque épreuve est identifiée de manière unique par son numéro **_numEp_**. Toutes les informations décrivant une épreuve dépendent donc de ce numéro.

**Dépendance fonctionnelle principale :**

_**numEp → nomEp, formeEp, categorieEp, nbSportifsEp, dateEp, nomDi**_
 numEp determine toutes les autre inforations

_**nomEp →  nomDi**_
nomEp determine nomDi 

_**\{numEp\}+ = \{numEp, nomEp, formeEp, categorieEp, nbSportifsEp, dateEp, nomDi}**_
La clé de la relation est  **\{numEp_\}

Comme **_nomEp_**  détermine **_nomDi_** et **_nomEp_** dépend de la clé donc **_nomDi_** est transitivement dépendant de la clé par l'intermédiaire de **_nomEp_** qui est un attribut non clé, donc la relation n'est pas en **3NF**.

Pour normaliser correctement, il faut décomposer la relation en deux relations :
### Relation 1 : LesEpreuves 

_**LesEpreuves**(<u>numEp</u>,nomEp, formeEp, categorieEp, nbSportifsEp, dateEp)_

### Relation 2 : LesDisciplines

_**LesDisciplines**(<u>nomEp</u>, nomDi)_


Ces deux relations sont alors en **BCNF**.

--- 
## 2. Relation LesSportifsEQ

La relation **LesSportifsEQ(numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, numEq)** regroupe les informations d’un sportif ainsi que l’équipe à laquelle il est associé.  
Chaque sportif est identifié par un numéro unique **_numSp_**. Toutes les informations personnelles du sportif en dépendent sauf **_numEq_**.

**Dépendance fonctionnelle certaine :**

**_numSp → nomSp, prenomSp, pays, categorieSp, dateNaisSp
nomSp, prenomSp → numSp , pays, categorieSp, dateNaisSp**

L’énoncé précise qu’un sportif peut appartenir à plusieurs équipes. donc, la dépendance :
numSp → numEq est fausse. 
numEq → pays n'est pas toujours vraie parce que numEq prend des valeurs NULL et avec on peut pas déterminer le pays.


_**\{numEq, numSp\}+ = \{numEq, numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp}**
**\{numEq, nomSp, prenomSp\}+ = \{numEq, nomSp, prenomSp, numSp, pays, categorieSp, dateNaisSp}**_

Les clés de la relation sont  **\{numEq, numSp\} et \{numEq, nomSp, prenomSp\}**


Comme on a des attributs qui dépendent d'une partie de la clé, donc la relation n'est pas en **2NF**.

Pour normaliser correctement, il faut décomposer la relation en deux relations :

### Relation 1 : LesSportifs

_**LesSportifs**(<u>numSp</u>, nomSp, prenomSp, pays, categorieSp, dateNaisSp)_

### Relation 2 : LesEquipes

_**LesEquipes**(<u>numSp, numEq</u>)_

On peut meme ajouter la relation PaysEq(numEq, Pays) mais on n'en aura pas vraiment besoin.


La première relation contient les informations personnelles du sportif.  
La seconde décrit l’association entre les sportifs et les équipes.  
Ces deux relations sont alors en **BCNF**.

--- 

# 2-  Implémentation 

## Question 3 – schéma relationnel : 


## Tables principales

  

**LesParticipants**(<ins>numPar</ins>)

/* $(np)$ ∈ LesParticipants ⇔ un participant est identifié par `np` */

  

**LesSportifs**(<ins>numSp</ins>, <ins>nomSp, prenomSp</ins>, pays, categorieSp, dateNaisSp)  

/* $(ns, n, p, pa, c, d)$ ∈ LesSportifs ⇔ un sportif identifié par `ns`, nommé `n`, prénom `p`, représentant le pays `pa`, de catégorie `c`, né le `d` */

  

**LesEquipes**(<ins>numEq</ins>)  

/* $(ne, nb)$ ∈ LesEquipes ⇔ une équipe identifiée par `ne` */

  

**LesSportifsEQ**(<ins>numSp, numEq</ins>)  

/* $(sp, eq)$ ∈ LesSportifsEQ ⇔ le sportif `sp` appartient à l'équipe `eq` */

  

**LesDisciplines**(<ins>nomDi</ins>)  

/* $(d)$ ∈ LesDisciplines ⇔ une discipline portant le nom `d` */

  

**LesEpreuves**(<ins>numEp</ins>, nomEp, formeEp, categorieEp, nbSportifsEp, dateEp, nomDi)  

/* $(e, n, f, c, nb, da, d)$ ∈ LesEpreuves ⇔ une épreuve identifiée par `e`, nommée `n`, de forme `f` (individuelle, par équipe, par couple), de catégorie `c` (masculin, feminin, mixte), avec nb sportifs `nb`, ayant lieu à la date `da`, faisant partie de la discipline `d` */

  

**LesResultats**(<ins>numPar, numEp</ins>, medaille)  

/* $(p, e, m)$ ∈ LesResultats ⇔ le participant `p` a obtenu la médaille `m` dans l'épreuve `e` */

  

**LesInscriptions**(<ins>numPar, numEp</ins>)  

/* $(p, e)$ ∈ LesInscriptions ⇔ le participant `p` est inscrit à l'épreuve `e` */

  

---

  

# Vues

  

**LesAgesSportifs**$(numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, ageSp)$

/* Vue calculant l'âge de chaque sportif */

  

**LesNbsEquipiers**$(numEq, nbEquipiersEq)$ 

/* Vue calculant le nombre d'équipiers par équipe */

  

**AgeMoyenEquipesOr**$(ageMoyen)$ 

/* Vue calculant l'âge moyen des équipes ayant gagné une médaille d'or */

  

**ClassementPays**$(pays, nbOr, nbArgent, nbBronze)$

/* Vue donnant le classement des pays selon leur nombre de médailles */

  

---

  

# Contraintes d'intégrité référentielle

$LesSportifs[numSp]   \cap  LesEquipes [numEq]$ = $\varnothing$ 

$LesSportifs[numSp] \cup LesEquipes[numEq]$= $LesParticipants[numPar]$

$LesSportifs[numSp] ⊆ LesParticipants[numPar]$  

$LesEquipes[numEq] ⊆ LesParticipants[numPar]$  

$LesSportifsEQ[numSp] ⊆ LesSportifs[numSp]$ 

$LesSportifsEQ[numEq] ⊆ LesEquipes[numEq]$ 

$LesEpreuves[nomDi] ⊆ LesDisciplines[nomDi]$ 

$LesResultats[numPar] ⊆ LesParticipants[numPar]$  

$LesResultats[numEp] ⊆ LesEpreuves[numEp]$

$LesInscriptions[numPar] ⊆ LesParticipants[numPar]$  

$LesInscriptions[numEp] ⊆ LesEpreuves[numEp]$

  

--- 

# Contraintes supplémentaires

  

**Contraintes de domaine :**

$- numSp ∈ [1000, 1500[$

$- numEq ∈ [1, 100[$

  

**Contraintes sur les équipes :**

- Une équipe contient au moins 2 sportifs

- Un sportif peut appartenir à plusieurs équipes

- Tous les sportifs d'une même équipe doivent représenter le même pays

- nbEquipiersEq est calculé via les vues

  

**Contraintes sur les épreuves :**

- Une épreuve individuelle n'admet que des sportifs (numPar ∈ [1000, 1500[)

- Une épreuve par équipe n'admet que des équipes (numPar ∈ [1, 100[)

- Une épreuve doit avoir au moins 3 inscrits pour attribuer les médailles

- La catégorie d'un participant doit être compatible avec celle de l'épreuve

  

**Contraintes sur les médailles :**

- medaille ∈ {gold, silver, bronze}

- Pas d'ex-aequo, toutes les médailles sont attribuées

- Un participant ne peut gagner qu'une seule médaille dans une épreuve

- Si silver est attribuée alors gold l'est aussi

- Si bronze est attribuée, gold et silver le sont aussi

  

**Contraintes sur les inscriptions :**

- Un participant doit être inscrit avant de recevoir un résultat

- Un sportif doit avoir au moins 18 ans pour participer

  

---

  

# Domaines et types énumérés

  

**Types de base :**

$- domaine(numPar) = domaine(numSp) = domaine(numEq) = domaine(numEp) = entier > 0$

$- domaine(nomSp, prenomSp, pays, nomEp, nomDi) = texte$

$- domaine(dateNaisSp, dateEp) = date$

$- domaine(nbEquipiersEq, nbSportifsEp) = entier ≥ 0$

  

**Types énumérés :**

$- TypeCat = {masculin, feminin, mixte}$

$- TypeForme = {individuelle, par equipe, par couple}$

$- TypeMed = {gold, silver, bronze}$

  

**Affectation des domaines :**

$- domaine(categorieSp) = {masculin, feminin}$

$- domaine(categorieEp) = TypeCat$

$- domaine(formeEp) = TypeForme$

$- domaine(medaille) = TypeMed$

  

---

  

# Triggers

  

**VerifAgeSportif** : Vérifie qu'un sportif a au moins 18 ans  

**VerifFormeEpreuve** : Vérifie la cohérence forme épreuve / type participant  

**InterditDoublonMedaille** : Empêche qu'un participant ait 2 résultats pour la même épreuve

