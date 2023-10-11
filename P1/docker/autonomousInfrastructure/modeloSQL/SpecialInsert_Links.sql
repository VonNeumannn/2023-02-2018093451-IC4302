CREATE OR REPLACE PROCEDURE INSERT_LINK(

    p_Link IN VARCHAR2,
    p_pageid IN INT
)
AS
    v_Link_id NUMBER;
    v_page_link_id NUMBER;
BEGIN


-- 5.1 Insertar link a su tabla
  BEGIN
    SELECT "LinkID" INTO v_Link_id FROM "ADMIN"."Link" WHERE "link" = p_Link;
    EXCEPTION
    WHEN NO_DATA_FOUND THEN
      v_Link_id:= NULL;
  END;

  IF v_Link_id IS NULL THEN
    -- Link does not exist, insert new one
    SELECT
      CASE WHEN MAX("LinkID") IS NULL THEN 0
          ELSE MAX("LinkID") + 1
      END INTO v_Link_id
    FROM "ADMIN"."Link";

    INSERT INTO "ADMIN"."Link" ("LinkID", "link")
      VALUES (v_link_id, p_Link);
  END IF;

    -- 5.2 Insertar en tabla de relaciones
    SELECT
    CASE WHEN MAX("PageLinkID") IS NULL THEN 0
        ELSE MAX("PageLinkID") + 1
    END INTO v_page_link_id
    FROM "ADMIN"."PageXLink";
    INSERT INTO "ADMIN"."PageXLink" ("PageLinkID", "PageID", "LinkID")
      VALUES (v_page_link_id, p_pageid, v_link_id);

END INSERT_LINK;