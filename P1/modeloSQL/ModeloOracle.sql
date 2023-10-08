DROP TABLE "PageXLink";
DROP TABLE "PageXRestrictions";
DROP TABLE "LastRevision";
DROP TABLE "Page";
DROP TABLE "Link";
DROP TABLE "Restriction";
DROP TABLE "wikiUser";
DROP TABLE "Site";
DROP TABLE "File";

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

CREATE INDEX "siteIndex" ON "Site" ("databaseName", "siteName");

CREATE TABLE "wikiUser" (
"userId" INT PRIMARY KEY,
"Username" VARCHAR2(200)
);

CREATE INDEX "wikiuserIndex" ON "wikiUser" ("Username");

CREATE TABLE "Restriction" (
"RestrictionId" INT PRIMARY KEY,
"RestrictionLink" VARCHAR2(1000)
);

CREATE INDEX "restrictionIndex" ON "Restriction" ("RestrictionLink");

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
"Restriction" INT,
"Title" VARCHAR2(500),
"WikipediaGenerated" VARCHAR2(200)
);

CREATE INDEX "pageIndex" ON "Page" ("Namespace");

CREATE TABLE "LastRevision" (
"Revision_id" INT PRIMARY KEY,
"wikiUserId" INT,
FOREIGN KEY ("wikiUserId") REFERENCES "wikiUser"("userId"),
"RevisionWikiText" CLOB,
"Redirect" VARCHAR2(1000),
"PageBytes" INT,
"RevisionDate" DATE,
"RevisionCleanText" CLOB,
"PageId" INT,
FOREIGN KEY ("PageId") REFERENCES "Page"("Pageid")
);

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