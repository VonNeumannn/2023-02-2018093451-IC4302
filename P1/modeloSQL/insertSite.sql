-- Para insertar un site, se supone que recibirá el file id como parámetro, regresa el siteid, esto es importante para crear los pages
CREATE OR REPLACE PROCEDURE "INSERT_SITE" (
  p_fileid INT,
  p_databasename VARCHAR2,
  p_sitename VARCHAR2,
  p_language VARCHAR2,
  p_siteid OUT INT
)
AS
BEGIN

    SELECT MAX('siteid') + 1 INTO p_siteid FROM "ADMIN"."Site";
  
    INSERT INTO "Site" ("Siteid", "Fileid", "databaseName", "siteName", "Language")
    VALUES (p_siteid, p_fileid, p_databasename, p_sitename, p_language);
  
END INSERT_SITE;


