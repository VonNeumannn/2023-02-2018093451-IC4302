import oracledb

# Función para conectar con Oracledb
# Regresa conexión con la base
def dbOracle_connection():
  cs = '''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=g25fe25c70e5806_ic4302_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''

  try:
    conn = oracledb.connect(user="ADMIN", password="thisiswrongNereo08", dsn=cs)
    print("Conectado")

    return conn

  except oracledb.DatabaseError as e:
    print("Couldn't connect to the database:", e)


# Se establece conexión con la base
conn = dbOracle_connection()
cursor = conn.cursor()

# Crean las tablas de la base de datos usando el modelo SQL definido en el archivo
f = open('modeloSQL/ModeloOracle.sql')
full_sql = f.read()
sql_commands = full_sql.split(';')

for sql_command in sql_commands:
  print("")
  print("-----------------------------")
  print("Se va a ejecutar el comando:")
  print(sql_command)
  try:
    cursor.execute(sql_command)
    conn.commit()
  except Exception as e:
    print(e)

# Por cada archivo en la lista de procedimientos se agrega el procedimiento a la base
lista_procedures = ['modeloSQL/insertFile.sql', 'modeloSQL/getFilenames.sql', 'modeloSQL/insertSite.sql', 'modeloSQL/busquedaGeneralSP.sql','modeloSQL/insertarPageALL.sql']
for procedure in lista_procedures:
  f = open(procedure)
  sql = f.read()
  print("")
  print("-----------------------------")
  print("Se va a ejecutar el comando:")
  print(sql)
  cursor.execute(sql)
  conn.commit()

print("")
print("-----------------------------")
print("Se creo la infrastructura exitosamente")

