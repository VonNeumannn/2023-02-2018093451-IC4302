-- Se reciben todos los datos relacionados a una página y se ingresan en sus respectivas tablas
CREATE OR REPLACE PROCEDURE INSERT_PAGE_ALL(
  -- Parámetros para Page
  p_pageid INT,
  p_siteid INT,
  p_namespace VARCHAR2,
  p_wikipedialink VARCHAR2,
  p_restriction INT,
  p_title VARCHAR2,
  p_wikipediagenerated VARCHAR2

  -- Parámetros para el Wikiuser
  p_userid INT,
  p_username VARCHAR2

  -- Parámetros para LastRevision
  p_revisionwikitext CLOB,
  p_redirect VARCHAR2,
  p_pagebytes INT,
  p_revisiondate DATE,
  p_revisioncleantext CLOB,
  p_pageid INT

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

  -- Cursor para links
  CURSOR c_links IS
    SELECT column_value FROM TABLE(p_links);

  -- Cursor para restricciones
  CURSOR c_restrictions IS
    SELECT column_value FROM TABLE(p_restrictions);

BEGIN

  -- 1. Insertar página
  INSERT INTO page (
    pageid, siteid,namespace,wikipedialink,title,wikipediagenerated)
  VALUES (p_pageid, p_siteid,p_namespace, p_wikipedialink,p_title,p_wikipediagenerated);

  -- 2. Insertar Wikiuser
  INSERT INTO wikiuser (userid,username)
  VALUES (p_userid,p_username);


  -- 3. Obtener nuevo ID de revisión
  SELECT MAX(revision_id) + 1 INTO v_revision_id FROM lastrevision;

  -- 4. Insertar última revisión
  -- Se usa el pageid y el wikiuserid de los datos recién registrados
   INSERT INTO lastrevision (
    revision_id,
    wikiuserid,
    revisionwikitext,
    redirect,
    pagebytes,
    revisiondate,
    revisioncleantext,
    pageid
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
    SELECT MAX(linkid) + 1 INTO v_link_id FROM link;

    INSERT INTO link (linkid, link)
      VALUES (v_link_id, r_link.column_value);

    -- 5.2 Obtener nuevo ID
    SELECT MAX(pagelinkid) + 1 INTO v_pagelink_id FROM pagexlink;

    -- 5.3 Insertar en tabla de relación
    INSERT INTO pagexlink (pagelinkid, pageid, linkid)
      VALUES (v_pagelink_id, p_pageid, v_link_id);

  END LOOP;


  -- 6. Recorrer restricciones

  FOR r_restriction IN c_restrictions LOOP

    -- 6.1 Insertar restricción
    SELECT MAX(restrictionid) + 1 INTO v_restriction_id FROM restriction;

    INSERT INTO restriction (restrictionid, restrictionlink)

    VALUES (v_restriction_id, r_restriction.column_value);

    -- 6.2 Obtener nuevo ID

    SELECT MAX(pagexrestrictions_id) + 1 INTO v_page_restriction_id FROM pagexrestrictions;

    -- 6.3 Insertar en tabla de relación

    INSERT INTO pagexrestrictions (pagexrestrictions_id, pageid, restrictionid)

    VALUES (v_page_restriction_id, p_pageid, v_restriction_id);

  END LOOP;

END INSERT_PAGE_ALL;