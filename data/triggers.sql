-- TRIGGER 1 : Verification age minimum (18 ans)
CREATE TRIGGER VerifAgeSportif
   BEFORE INSERT ON LesSportifs
   FOR EACH ROW
   WHEN (
      CAST(strftime('%Y', 'now') AS INTEGER) - 
      CAST(strftime('%Y', NEW.dateNaisSp) AS INTEGER) < 18
   )
BEGIN
   SELECT RAISE(ABORT, 'Le sportif doit avoir au moins 18 ans pour participer');
END;

/

-- TRIGGER 2 : Coherence forme epreuve et type participant
CREATE TRIGGER VerifFormeEpreuve
   BEFORE INSERT ON LesInscriptions
   FOR EACH ROW
   WHEN (
      (SELECT formeEp FROM LesEpreuves WHERE numEp = NEW.numEp) = 'individuelle'
      AND NEW.numPar < 1000
   ) OR (
      (SELECT formeEp FROM LesEpreuves WHERE numEp = NEW.numEp) = 'par equipe'
      AND NEW.numPar > 1000
   )
BEGIN
   SELECT RAISE(ABORT, 'La forme de l''épreuve ne correspond pas au type de participant');
END;

/

-- TRIGGER 3 : Interdire les doublons de medailles
CREATE TRIGGER InterditDoublonMedaille
   BEFORE INSERT ON LesResultats
   FOR EACH ROW
   WHEN EXISTS (
      SELECT 1
      FROM LesResultats R
       WHERE R.numPar = NEW.numPar 
         AND R.numEp = NEW.numEp
   )
BEGIN
   SELECT RAISE(ABORT, 'Ce participant a deja un resultat pour cette epreuve');
END;