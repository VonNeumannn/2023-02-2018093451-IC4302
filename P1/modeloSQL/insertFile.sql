-- Método para agregar un File, retorna su id, importante para ingresarlo luego en la tabla Site
CREATE OR REPLACE PROCEDURE INSERT_FILE (
  p_filename IN VARCHAR2,
  p_fileid OUT INT
)
AS
BEGIN

  SELECT MAX(fileid) + 1 INTO p_fileid FROM file;

  INSERT INTO file (fileid, filename)
  VALUES (p_fileid, p_filename);

END INSERT_FILE;
