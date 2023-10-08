CREATE OR REPLACE PROCEDURE BUSCAQUEDAGENERAL
(
  INPATRON IN VARCHAR2
, OUTRESULTCODE OUT NUMBER
, OUT_RESULT_CURSOR OUT SYS_REFCURSOR
) AS
BEGIN
    OUTRESULTCODE := 0;
    OPEN OUT_RESULT_CURSOR FOR
    SELECT LR."Revision_id",
       P."Pageid",
       S."Siteid"
    FROM "ADMIN"."LastRevision" LR
    INNER JOIN "ADMIN"."Page" P
    ON LR."PageId" = P."Pageid"
    INNER JOIN "ADMIN"."Site" S
    ON P."Siteid" = S."Siteid"
    WHERE CONTAINS(LR."RevisionCleanText", 'a', 1) > 0
        OR CONTAINS(LR."Redirect",'b', 2) > 0
        OR CONTAINS(P."Namespace",'a', 3) > 0
        OR CONTAINS(P."WikipediaLink",'', 4) > 0
        OR CONTAINS(P."Title",'a', 5) > 0
        OR CONTAINS(P."WikipediaGenerated",'', 6) > 0
        OR CONTAINS(S."siteName",'a', 7) > 0
        OR CONTAINS(S."Language",'a', 8) > 0;

END BUSCAQUEDAGENERAL;