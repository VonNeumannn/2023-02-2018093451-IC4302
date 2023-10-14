import oracledb

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

# Crear Estructura
lista_estructura = ['modeloSQL/ModeloOracle.sql']
for archivo in lista_estructura:
  f = open(archivo)
  full_sql = f.read()
  sql_commands = full_sql.split(';')

  for sql_command in sql_commands:
    print(sql_command)
    try:
      cursor.execute(sql_command)
      conn.commit()
    except Exception as e:
      print(e)

lista_procedures = ['modeloSQL/insertFile.sql', 'modeloSQL/getFilenames.sql', 'modeloSQL/insertSite.sql', 'modeloSQL/busquedaGeneralSP.sql','modeloSQL/insertarPageALL.sql',
                    'modeloSQL/SpecialInsert_Links.sql', 'modeloSQL/SpecialInsert_Restriction.sql']
for procedure in lista_procedures:
  f = open(procedure)
  sql = f.read()
  print(sql)
  cursor.execute(sql)
  conn.commit()
print("")
print("-----------------------------")
print("Se creo la infrastructura exitosamente")


