DROP TABLE "PageXLink";
DROP TABLE "PageXRestrictions";
DROP TABLE "LastRevision";
DROP TABLE "Page";
DROP TABLE "Link";
DROP TABLE "Restriction";
DROP TABLE "Site";
DROP TABLE "File";
--DROP INDEX IDX_REVISIONCLEANTEXT;
--DROP INDEX IDX_REDIRECT;
--DROP INDEX IDX_NAMESPACE;
--DROP INDEX IDX_WIKIPEDIALINK;
--DROP INDEX IDX_TITLE;
--DROP INDEX IDX_WIKIPEDIAGENERATED;
--DROP INDEX IDX_SITENAME;
--DROP INDEX IDX_LANGUAGE;

CREATE TABLE "File" (
"Fileid" INT PRIMARY KEY,
"Filename" VARCHAR2(500)
);

CREATE TABLE "Site" (
"Siteid" INT PRIMARY KEY,
"Fileid" INT,
FOREIGN KEY ("Fileid") REFERENCES "File"("Fileid"),
"databaseName" VARCHAR2(500),
"siteName" VARCHAR2(500),
"Language" VARCHAR2(25)
);
CREATE INDEX idx_siteName ON "ADMIN"."Site" ("siteName") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_Language ON "ADMIN"."Site" ("Language") INDEXTYPE IS CTXSYS.CONTEXT;

CREATE TABLE "Restriction" (
"RestrictionId" INT PRIMARY KEY,
"RestrictionLink" VARCHAR2(1000)
);

CREATE TABLE "Link" (
"LinkID" INT PRIMARY KEY,
"link" VARCHAR2(1000)
);

CREATE TABLE "Page" (
"Pageid" INT PRIMARY KEY,
"Siteid" INT,
FOREIGN KEY ("Siteid") REFERENCES "Site"("Siteid"),
"Namespace" VARCHAR2(500),
"WikipediaLink" VARCHAR2(1000),
"Title" VARCHAR2(500),
"WikipediaGenerated" VARCHAR2(200),
"Rating" INT DEFAULT 0
);
CREATE INDEX idx_Namespace ON "ADMIN"."Page" ("Namespace") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_WikipediaLink ON "ADMIN"."Page" ("WikipediaLink") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_Title ON "ADMIN"."Page" ("Title") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_WikipediaGenerated ON "ADMIN"."Page" ("WikipediaGenerated") INDEXTYPE IS CTXSYS.CONTEXT;

CREATE TABLE "LastRevision" (
"Revision_id" INT PRIMARY KEY,
"Username" VARCHAR2(200),
"RevisionWikiText" CLOB,
"Redirect" VARCHAR2(1000) NULL,
"PageBytes" INT,
"RevisionDate" DATE NULL,
"RevisionCleanText" CLOB,
"PageId" INT,
FOREIGN KEY ("PageId") REFERENCES "Page"("Pageid")
);

CREATE INDEX idx_Redirect ON "ADMIN"."LastRevision" ("Redirect") INDEXTYPE IS CTXSYS.CONTEXT;
CREATE INDEX idx_RevisionCleanText ON "ADMIN"."LastRevision"("RevisionCleanText") INDEXTYPE IS CTXSYS.CONTEXT;

CREATE TABLE "PageXRestrictions" (
"PageXRestrictions_id" INT PRIMARY KEY,
"PageId" INT,
"RestrictionId" INT,
FOREIGN KEY ("PageId") REFERENCES "Page"("Pageid"),
FOREIGN KEY ("RestrictionId") REFERENCES "Restriction"("RestrictionId")
);

CREATE TABLE "PageXLink" (
"PageLinkID" INT PRIMARY KEY,
"PageID" INT,
"LinkID" INT,
FOREIGN KEY ("PageID") REFERENCES "Page"("Pageid"),
FOREIGN KEY ("LinkID") REFERENCES "Link"("LinkID")
);

CREATE OR REPLACE TYPE "STRING_VARRAY2" AS VARRAY(2000) OF VARCHAR2(1000);