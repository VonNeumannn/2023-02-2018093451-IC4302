CREATE OR REPLACE PROCEDURE INSERT_PAGE_ALL(
  -- ParÃ¡metros para Page
  p_pageid INT,
  p_siteid INT,
  p_namespace VARCHAR2,
  p_wikipedialink VARCHAR2,
  p_restriction INT,
  p_title VARCHAR2,
  p_wikipediagenerated VARCHAR2,

  -- ParÃ¡metros para el Wikiuser
  p_userid INT,
  p_username VARCHAR2,

  -- ParÃ¡metros para LastRevision
  p_revisionwikitext CLOB,
  p_redirect VARCHAR2,
  p_pagebytes INT,
  p_revisiondate DATE,
  p_revisioncleantext CLOB,

  -- Lista de links
  p_links SYS.ODCIVARCHAR2LIST,

  -- Lista de restricciones
  p_restrictions SYS.ODCIVARCHAR2LIST

)
AS
   -- Variables
  v_revision_id INT;
  v_link_id INT;
  v_pagelink_id INT; 
  v_restriction_id INT;
  v_page_restriction_id INT;

  -- Cursor para links
  CURSOR c_links IS
    SELECT column_value FROM TABLE(p_links);

  -- Cursor para restricciones
  CURSOR c_restrictions IS
    SELECT column_value FROM TABLE(p_restrictions);

BEGIN

  -- 1. Insertar pÃ¡gina
  INSERT INTO "ADMIN"."Page" (
    "Pageid", "Siteid","Namespace","WikipediaLink","Title","WikipediaGenerated")
  VALUES (p_pageid, p_siteid,p_namespace, p_wikipedialink,p_title,p_wikipediagenerated);

  -- 2. Insertar Wikiuser
  INSERT INTO "ADMIN"."wikiUser" ("userId","Username")
  VALUES (p_userid,p_username);

  SELECT
  -- 3. Obtener nuevo ID de revisiÃ³n
  CASE WHEN MAX("Revision_id") IS NULL THEN 0
       ELSE MAX("Revision_id") + 1
  END INTO v_revision_id FROM "ADMIN"."LastRevision";

  -- 4. Insertar Ãºltima revisiÃ³n
  -- Se usa el pageid y el wikiuserid de los datos reciÃ©n registrados
   INSERT INTO "ADMIN"."LastRevision" (
    "Revision_id",
    "wikiUserId",
    "RevisionWikiText",
    "Redirect",
    "PageBytes",
    "RevisionDate",
    "RevisionCleanText",
    "PageId"
  ) VALUES (
    v_revision_id,
    p_userid,
    p_revisionwikitext,
    p_redirect,
    p_pagebytes,
    p_revisiondate,
    p_revisioncleantext,
    p_pageid
  );

  -- 5. Recorrer links
  -- Por cada link en la lista
  FOR r_link IN c_links LOOP

    -- 5.1 Insertar link a su tabla
    SELECT 
    CASE WHEN MAX("LinkID") IS NULL THEN 0
        ELSE MAX("LinkID") + 1
    END INTO v_link_id FROM "ADMIN"."Link";

    INSERT INTO "ADMIN"."Link" ("LinkID", "link")
      VALUES (v_link_id, r_link.column_value);

    -- 5.2 Obtener nuevo ID
    SELECT
    CASE WHEN MAX("PageLinkID") IS NULL THEN 0  
        ELSE MAX("PageLinkID") + 1
    END INTO v_pagelink_id FROM "ADMIN"."PageXLink";

    -- 5.3 Insertar en tabla de relaciÃ³n
    INSERT INTO "ADMIN"."PageXLink" ("PageLinkID", "PageID", "LinkID")
      VALUES (v_pagelink_id, p_pageid, v_link_id);

  END LOOP;


  -- 6. Recorrer restricciones

  FOR r_restriction IN c_restrictions LOOP

    -- 6.1 Insertar restricciÃ³n
    SELECT
    CASE WHEN MAX("RestrictionId") IS NULL THEN 0
        ELSE MAX("RestrictionId") + 1 
    END INTO v_restriction_id FROM "ADMIN"."Restriction";

    INSERT INTO "ADMIN"."Restriction" ("RestrictionId", "RestrictionLink")

    VALUES (v_restriction_id, r_restriction.column_value);

    -- 6.2 Obtener nuevo ID

    SELECT
    CASE WHEN MAX("PageXRestrictions_id") IS NULL THEN 0
        ELSE MAX("PageXRestrictions_id") + 1
    END INTO v_page_restriction_id FROM "ADMIN"."PageXRestrictions";

    -- 6.3 Insertar en tabla de relaciÃ³n

    INSERT INTO "ADMIN"."PageXRestrictions" ("PageXRestrictions_id", "PageId", "RestrictionId")

    VALUES (v_page_restriction_id, p_pageid, v_restriction_id);

  END LOOP;

END INSERT_PAGE_ALL;