CREATE OR REPLACE PROCEDURE INSERT_PAGE_ALL(
  -- Parametros para crear un page y tablas relacionadas
  p_pageid INT,
  p_siteid INT,
  p_namespace VARCHAR2,
  p_wikipedialink VARCHAR2,
  p_title VARCHAR2,
  p_wikipediagenerated VARCHAR2,

  p_username VARCHAR2,

  -- Parametros para LastRevision
  p_revisionwikitext CLOB,
  p_redirect VARCHAR2,
  p_pagebytes INT,
  p_revisiondate DATE,
  p_revisioncleantext CLOB

)
AS
   -- Variables
  v_revision_id INT;
  user_count INT;
BEGIN

  -- 1. Insertar pÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡gina
  INSERT INTO "ADMIN"."Page" (
    "Pageid", "Siteid","Namespace","WikipediaLink","Title","WikipediaGenerated")
  VALUES (p_pageid, p_siteid,p_namespace, p_wikipedialink,p_title,p_wikipediagenerated);


  SELECT
  -- 3. Obtener nuevo ID de revision
  CASE WHEN MAX("Revision_id") IS NULL THEN 0
       ELSE MAX("Revision_id") + 1
  END INTO v_revision_id FROM "ADMIN"."LastRevision";

  -- 4. Insertar una nueva entrada a la tabla de ultima revisión
  -- Se usa el pageid de los datos previamente ingresados
   INSERT INTO "ADMIN"."LastRevision" (
    "Revision_id",
    "Username",
    "RevisionWikiText",
    "Redirect",
    "PageBytes",
    "RevisionDate",
    "RevisionCleanText",
    "PageId"
  ) VALUES (
    v_revision_id,
    p_username,
    p_revisionwikitext,
    p_redirect,
    p_pagebytes,
    p_revisiondate,
    p_revisioncleantext,
    p_pageid
  );

END INSERT_PAGE_ALL;