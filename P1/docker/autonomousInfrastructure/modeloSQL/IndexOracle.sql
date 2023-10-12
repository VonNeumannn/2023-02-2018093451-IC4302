CREATE INDEX idx_RevisionCleanText ON "ADMIN"."LastRevision"("RevisionCleanText") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_Redirect ON "ADMIN"."LastRevision" ("Redirect") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_Namespace ON "ADMIN"."Page" ("Namespace") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_WikipediaLink ON "ADMIN"."Page" ("WikipediaLink") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_Title ON "ADMIN"."Page" ("Title") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_WikipediaGenerated ON "ADMIN"."Page" ("WikipediaGenerated") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_siteName ON "ADMIN"."Site" ("siteName") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_Language ON "ADMIN"."Site" ("Language") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE OR REPLACE TYPE "STRING_VARRAY2" AS VARRAY(2000) OF VARCHAR2(1000);