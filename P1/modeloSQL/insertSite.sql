-- Para insertar un site, se supone que recibirá el file id como parámetro, regresa el siteid, esto es importante para crear los pages
CREATE OR REPLACE PROCEDURE INSERT_SITE(
  p_fileid INT,p_databasename VARCHAR2,p_sitename VARCHAR2, p_language VARCHAR2, p_siteid OUT INT)
AS
BEGIN

  SELECT MAX(siteid) + 1 INTO p_siteid FROM site;

  INSERT INTO site (
    siteid,fileid,databasename,sitename,language)
    VALUES (p_siteid,p_fileid,p_databasename,p_sitename,p_language);

END INSERT_SITE;

import oracledb
import re

def dbOracle_connection():
  cs = '''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=g25fe25c70e5806_ic4302_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''

  try:
    conn = oracledb.connect(user="ADMIN", password="thisiswrongNereo08", dsn=cs)
    print("Conectado")

    return conn

  except oracledb.DatabaseError as e:
    print("Couldn't connect to the database:", e)


conn = dbOracle_connection()
cursor = conn.cursor()
cursor.execute("""DROP TABLE "PageXLink";""")

# Crear Estructura
f = open('ModeloOracle.sql')
full_sql = f.read()
sql_commands = full_sql.split(';')

for sql_command in sql_commands:
  try:
    cursor.execute(sql_command)
    conn.commit()
  except Exception as e:
    print(e)

lista_procedures = ['insertFile.sql', 'getFilenames.sql', 'insertSite.sql', 'busquedaGeneralSP.sql','insertarPageALL.sql']
for procedure in lista_procedures:
  f = open(procedure)
  sql = f.read()
  print(sql)
  cursor.execute(sql)
  conn.commit()
  print('-------------')

