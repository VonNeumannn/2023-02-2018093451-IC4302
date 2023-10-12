CREATE OR REPLACE PROCEDURE INSERT_RESTRICTION(

    p_Restriction IN VARCHAR2,
    p_pageid IN INT
)
AS
    v_restriction_id INT;
    v_page_restriction_id INT;
BEGIN
    BEGIN
    SELECT "RestrictionId" INTO v_restriction_id FROM "ADMIN"."Restriction" WHERE "RestrictionLink" = p_Restriction;
    EXCEPTION
    WHEN NO_DATA_FOUND THEN
      v_restriction_id:= NULL;
    END;


    IF v_restriction_id IS NULL THEN

        -- Restriction does not exist, insert new one
        SELECT
        CASE WHEN MAX("RestrictionId") IS NULL THEN 0
             ELSE MAX("RestrictionId") + 1
        END INTO v_restriction_id
        FROM "ADMIN"."Restriction";

        INSERT INTO "ADMIN"."Restriction"
        ("RestrictionId", "RestrictionLink")
        VALUES
        (v_restriction_id, p_Restriction);

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

END INSERT_RESTRICTION;