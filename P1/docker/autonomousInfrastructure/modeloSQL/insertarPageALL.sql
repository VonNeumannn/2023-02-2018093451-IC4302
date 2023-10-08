CREATE OR REPLACE PROCEDURE INSERT_PAGE_ALL(
  -- ParÃƒÆ’Ã‚Â¡metros para Page
  p_pageid INT,
  p_siteid INT,
  p_namespace VARCHAR2,
  p_wikipedialink VARCHAR2,
  p_title VARCHAR2,
  p_wikipediagenerated VARCHAR2,

  -- ParÃƒÆ’Ã‚Â¡metros para el Wikiuser
  p_userid INT,
  p_username VARCHAR2,

  -- ParÃƒÆ’Ã‚Â¡metros para LastRevision
  p_revisionwikitext CLOB,
  p_redirect VARCHAR2,
  p_pagebytes INT,
  p_revisiondate DATE,
  p_revisioncleantext CLOB,

  -- Lista de links
  p_links string_varray,

  -- Lista de restricciones
  p_restrictions string_varray

)
AS
   -- Variables
  v_revision_id INT;
  v_link_id INT;
  v_pagelink_id INT;
  v_restriction_id INT;
  v_page_restriction_id INT;
  user_count INT;
  link_id INT;
  restriction_id NUMBER;

BEGIN

  -- 1. Insertar pÃƒÆ’Ã‚Â¡gina
  INSERT INTO "ADMIN"."Page" (
    "Pageid", "Siteid","Namespace","WikipediaLink","Title","WikipediaGenerated")
  VALUES (p_pageid, p_siteid,p_namespace, p_wikipedialink,p_title,p_wikipediagenerated);

  -- 2. Insertar Wikiuser solo si no existe
  SELECT COUNT(*) INTO user_count
  FROM "ADMIN"."wikiUser"
  WHERE "userId" = p_userid;

  IF user_count = 0 THEN

    -- User does not exist, insert new row
    INSERT INTO "ADMIN"."wikiUser" ("userId", "Username")
    VALUES (p_userid, p_username);

  END IF;

  SELECT
  -- 3. Obtener nuevo ID de revisión
  CASE WHEN MAX("Revision_id") IS NULL THEN 0
       ELSE MAX("Revision_id") + 1
  END INTO v_revision_id FROM "ADMIN"."LastRevision";

  -- 4. Insertar ÃƒÆ’Ã‚Âºltima revisiÃƒÆ’Ã‚Â³n
  -- Se usa el pageid y el wikiuserid de los datos reciÃƒÆ’Ã‚Â©n registrados
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
  FOR i IN 1..p_links.COUNT LOOP

    -- 5.1 Insertar link a su tabla
      SELECT "LinkID" INTO link_id
      FROM "ADMIN"."Link"
      WHERE "link" = p_links(i);

      IF link_id IS NULL THEN
        -- Link does not exist, insert new one
        SELECT
          CASE WHEN MAX("LinkID") IS NULL THEN 0
              ELSE MAX("LinkID") + 1
          END INTO v_link_id
        FROM "ADMIN"."Link";

        INSERT INTO "ADMIN"."Link" ("LinkID", "link")
          VALUES (v_link_id, p_links(i));

      ELSE
        -- Link exists, use existing ID
        v_link_id := link_id;

      END IF;

    -- 5.2 Insertar en tabla de relaciÃƒÆ’Ã‚Â³n
    SELECT
    CASE WHEN MAX("PageLinkID") IS NULL THEN 0
        ELSE MAX("PageLinkID") + 1
    END INTO v_pagelink_id
    FROM "ADMIN"."PageXLink";
    INSERT INTO "ADMIN"."PageXLink" ("PageLinkID", "PageID", "LinkID")
      VALUES (v_pagelink_id, p_pageid, v_link_id);

  END LOOP;


  -- 6. Recorrer restricciones

  FOR i IN 1..p_restrictions.COUNT LOOP

    -- Check if restriction exists
    SELECT "RestrictionId" INTO restriction_id
    FROM "ADMIN"."Restriction"
    WHERE "RestrictionLink" = p_restrictions(i);

    IF restriction_id IS NULL THEN

      -- Restriction does not exist, insert new one
      SELECT
        CASE WHEN MAX("RestrictionId") IS NULL THEN 0
             ELSE MAX("RestrictionId") + 1
        END INTO v_restriction_id
      FROM "ADMIN"."Restriction";

      INSERT INTO "ADMIN"."Restriction"
        ("RestrictionId", "RestrictionLink")
      VALUES
        (v_restriction_id, p_restrictions(i));

    ELSE
      -- Restriction exists, use existing ID
      v_restriction_id := restriction_id;

    END IF;

    -- Insert relation
    SELECT
      CASE WHEN MAX("PageXRestrictions_id") IS NULL THEN 0
           ELSE MAX("PageXRestrictions_id") + 1
      END INTO v_page_restriction_id
    FROM "ADMIN"."PageXRestrictions";

    INSERT INTO "ADMIN"."PageXRestrictions"
      ("PageXRestrictions_id", "PageId", "RestrictionId")
    VALUES
      (v_page_restriction_id, p_pageid, v_restriction_id);

  END LOOP;

END INSERT_PAGE_ALL;