import bz2
import sys
import mwxml
from io import BytesIO
import oci
import os
import time
import tempfile
from pymongo import MongoClient
import certifi
import mwparserfromhell
import oracledb
from datetime import datetime

# LLave y datos para conectar con Oracle Cloud Infrastructure
#--------------------------------------------------------------------------------------------------------------------------
config = {
  "key_content": """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCyeqoVhQp5uJUk
R5/E1gqkckWVDk91rbYmJurpooXp2k98PZNPtrfz0ojtUiwEotBR9theADGuLLsY
E2tAj2jvqDoKofReMGjbk4BD+gIrlyfIRHTUdCTWfxY4dBG18i3pNB7alzbFxOv2
/V97iMdl4JYHL5MdWa3O7W+ILIgWgePIctD0iv2zObiBrZkBA0nCda42ordr5Srw
mrkCyr1DMCJJeiaFweGu6L193nOkI2FW33NUpd8MzuK3Euj4YJKCj9GlyfEtEJ9M
sG8VWehk79kamgtgnP/hdWQbLCyh4u4qzaZQDJGtjGHeIJ+qGHYffxRGt0i4jHfW
AT5cBcpDAgMBAAECggEAV+ZSouORa64tAZ+mv4Xc2u2OeGECYEYLydFr62HICwqi
D+GxjdZC1XnQRvUryaK3704fdHgq/4l3IV3a+gJHH5Td9QObOtIjqlSEHLZh4D8C
8D5KvaFvzRXtByOe31llJA+vzF8hshgQUGWr40bTUUjhCqvzC8bxc1J7lfi8kzxV
t2JCdgHdgcRN/ZnBsqTM9LZcrUkDNz3FR0jVjUYaBSLA0r+NEzjAJ2tvbOIxkgPQ
MK1GGnc0fotMBmSbrIzYXRaNeH2fCRu6v6oUtNbkOgV7i7wAhrIw9YQi1RMbOGyg
qYV/Htk2oN0gbgpWlX+G49ET4aAkCDiVsQQB0CI4xQKBgQDYNEihwFDyt0PX+P3l
Y5LOUV3z5DYjD+Eh09o3EW5iSanA0QJ4gIBmoZ6qc1aR4M4w7sQZ9XLxVFkDI5wK
jvYQSYGup5u5cdQa5YL8MuysPtw/3JFgLeE2JXwBEyjUWMaIZ/6mezJdy4sYOQ4u
OnuiHk8Y+1dDoay30JLF4NtVHQKBgQDTVL611KNYTJLLj1bAdvrOYo5FvHVbDnlQ
Z2PhmXN9N4jxZBi1tDajq+wFMr0I9GfaqubnbjPsn8BpqEuXGEDRTt0LXmFtUIc+
oXmkt/Dml7qWUV7Sfjk5Exaz5yAvcDPOeZiOfvjESlp1dfwZY9t3wUai44Eg5/Zi
GppeYq5e3wKBgDvVVFh3Wa+iKkNl5BYMlX9Fo2Owv466gUqUT6q3xz2qNzFmZnGk
1mQQzFFNtCKQ/V8rZNfuRo4lErE8tJ1zbQOa5CnKttz+dH2xEKvtB/SvPNLrnsvo
RpBulT/S5pTFsMPlS+MU6x5sCyV7/MGsa7S1AJzgSgksgBkqvsPGc8y9AoGAJROX
KfuWdOVqU8BgLgAx3Ie6Ak4gIMuXSR36jhgIBQ37Pq6bDzYA6BI/pGHUfH+0wM5/
GFdjUL5uWZsnN+kPZil56oayfSVFtR1LZDTJVQuFtt2rzy5KB9NrhkCkiu4aiL0Y
oNdx+a451KXQhvvYA1irdeSIQSexOGEGeEzD3u0CgYAV2F1lWiOBNMxZ2bNSt8Lw
lO0I1+CFfFCOulEPrMBk5De6akzVS9JT9lGxtQ2fHVtf+3IqnTz69j0WRvD4lYgX
phlZ2+9xGUxOrHdnzol50f/lQ0TmHM920nTp1XChosWS9vqUFE6OEYpNgQMkcFda
rvLR0LOLOhVbGpy/8zzQ/w==
-----END PRIVATE KEY-----""",
  "user": "ocid1.user.oc1..aaaaaaaashik7hmu6usm4tpruwrubbs6h6e5lyix6lcu67odiuc7vbfcvotq",
  "fingerprint": "06:25:27:f2:e2:81:c8:f2:18:9e:8a:d1:65:8c:5b:4d",
  "tenancy": "ocid1.tenancy.oc1..aaaaaaaaazrw3t5sa6dacgzzh573u763zxazhcnve2ndfdgaebwgh6dxlptq",
  "region": "us-ashburn-1"
}

# FUNCIONES Para manejo de Objetos del Bucket
#-----------------------------------------------------------------------------------------------------------------------
# Funcion para conectar con el bucket de oracle
# Usa los datos de configuracion definidos y establece una conexión con el bucket
def connect_Bucket():
    oci.config.validate_config(config)
    object_storage = oci.object_storage.ObjectStorageClient(config)
    return object_storage

# Esta función regresa una lista de todos los archivos del bucket
# Input: Una conexión con el bucket y el nombre del mismo
# Output: Lista de objetos del bucket
def get_files_in_bucket(object_storage,bucket_name):
    namespace = object_storage.get_namespace().data # The OCI namespace for your tenancy

    list_objects_response = object_storage.list_objects(namespace, bucket_name)
    objects = list_objects_response.data.objects

    return objects

# Esta función obtiene los nombres de todos los objetos en la lista del bucket, importante para comparar con las bases
# Recibe una lista de objetos generada por  get_files_in_bucket()
# Retorna una lista solo con los nombres de esos objetos
def get_bucket_objNames(objectlist):
    names = []
    for obj in objectlist:
        names.append(obj.name)

    return names

# Esta función recibe el nombre de un elemento específico en el bucket
# Lo descarga para que posteriormente sea descomprimido
# Se guarda en un archivo temporal
# Se regresa el nombre del archivo temporal en el sistema
def downloadFile(object_storage, bucket_name, object_name):
    namespace = object_storage.get_namespace().data
    obj = object_storage.get_object(namespace, bucket_name, object_name)

    # Bytes del objeto a archivo temporal
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(obj.data.content)
    temp_file.close()

    return temp_file.name

# Función para descomprimir un archivo con bz2,
# Recibe un bz2 y regresa un archivo binario descomprimido
# En lugar de subir descomprimido al bucket se descomprime aqui para ahorrar tiempo
def decompress_file(input_file):
    with bz2.open(input_file, 'rb') as f_in:
        return f_in.read()

#-----------------------------------------------------------------------------------------------------------------------
# FUNCIONES PARA PARSEAR TEXTO DEL DUMP
#-----------------------------------------------------------------------------------------------------------------------

# Se recibe una página del dump y se obtienen los datos de su última modificación
def get_last_revision(page):
    last_rev = None

    # Por cada revisión de la página
    for revision in page:
        last_rev = revision

    # El último valor asignado a la variable se retorna
    return last_rev

def parse_text(wiki_text):
    parsed = mwparserfromhell.parse(wiki_text)

    # Strip wiki markup, keep only plain text
    plain_text = parsed.strip_code(normalize=True, collapse=True)

    return plain_text

# Para obtener todos los links del texto
# En lugar de tener que usar otro documento, usamos mwparserfromhell para obtener los links usando el wikitext del page
# Se recibe el wikitext
# Se retorna una lista con cada uno de los links
# MEJORAR: Se debe hacer que se remuevan todos los espacios vacíos del link
def get_links(text):

    parsed = mwparserfromhell.parse(text)
    links = []

    # Encontrar todos los wikilinks
    for link in parsed.filter_wikilinks():
        # Obtener titulo del link
        title = link.title.strip()

        # Generar URL
        url = f'https://en.wikipedia.org/wiki/{title}'

        links.append(url)

    return links

# Función para extraer todos los datos relacionados con una página en el dump
# Recibe el dump.Page y extrae sys datos usando mwxml y mwparserfromhell
# Regresa un diccionario que contiene todos sus datos
def process_page(page):

  page_data = {}
  page_data["Title"] = page.title
  page_data["PageId"] = page.id
  page_data["Namespace"] = page.namespace

  # Se obtienen los datos de la última revisión
  last_revision = get_last_revision(page)

  # Se guardan en el diccionario
  page_data['LastRevisionData'] = {
    'User': {
      'UserID': last_revision.user.id,
      'username': last_revision.user.text
    },
    'Text': {
      'wikiText': last_revision.text,
      'NormalText': parse_text(last_revision.text)
    },
    'PageBytes': last_revision.bytes,
    'Redirect': page.redirect,
    'RevisionDate': str(last_revision.timestamp)
  }

  # Otros datos
  page_data['Restrictions'] = page.restrictions
  page_data['Links'] = get_links(last_revision.text)

  page_data['WikipediaLink'] = f'https://en.wikipedia.org/wiki/{page.title}'
  page_data['WikipediaGenerated'] = f'http://en.wikipedia.org/?curid={page.id}'

  return page_data


# Para procesar un archivo completo de los XML Dumps
# Esta función procesa todas las páginas dentro del dump y las ingresa en una o ambas bases de datos
# Recibe el objeto del dump
# Recibe una opción de almacenamiento, esto determina la base donde se guarda "SQL", "MONGO" y "AMBOS"
# Recibe el nombre del archivo que se va a procesar
def process_file(file_obj, opcionAlmacenamiento, filename):

    # Se descomprime el archivo
    binary_data = decompress_file(file_obj)
    # Lo convierte en datos que se puedan leer con mwxml.Dump
    bytes_io = BytesIO(binary_data)

    dump = mwxml.Dump.from_file(bytes_io)

    # Se determinan datos generales del archivo como nombre, dbname, sitename, Language
    filename_Dat = {"Filename": filename}
    filename_Dat['FileData'] = {'dbName': dump.site_info.dbname, 'siteName': dump.site_info.name, 'Language': "English"}

    # Al crear un site en SQL se regresa su id para asignarlo a todos los pages
    SQLsiteID = None

    # En esta sección se ingresa el nombre del archivo a procesar en la base
    # Esto permite luego revisar si los datos de un archivo ya han sido ingresados a una de las bases

    # Si solo se almacena en la base SQL
    if opcionAlmacenamiento == "SQL":
        SQLsiteID = insertFileSQL(filename_Dat)

    # Si solo se almacena en la base MONGO
    elif opcionAlmacenamiento == 'MONGO':
        insertarFileMongo(filename_Dat)

    # Si se quiere almacenar en ambas
    else:
        SQLsiteID = insertFileSQL(filename_Dat)
        insertarFileMongo(filename_Dat)

    # Una vez se almaceno el nombre del archivo se pasa a procesar y almacenar cada una de las páginas
    # Por cada página en el dump

    # Como son muchas páginas se puede configurar que se inserte cierta cantidad por archivo
    cont = 0
    for page in dump:

        # Se procesa la página
        processed = process_page(page)
        # Se agregan datos del archivo (Se usan para guardarlos en Mongo)
        processed['FileData'] = {'dbName': dump.site_info.dbname, 'siteName': dump.site_info.name, 'Language': "English" }

        print()
        print('------------------------------------------')
        print("Se esta procesando la página -->" + processed["Title"])

        # Se quiere guardar dependiendo de la opción
        if opcionAlmacenamiento == 'AMBOS':
            insertarPageSQL(processed, SQLsiteID)
            insertarPageMongo(processed)


        elif opcionAlmacenamiento == "SQL":
            insertarPageSQL(processed, SQLsiteID)

        elif opcionAlmacenamiento == 'MONGO':
            insertarPageMongo(processed)

        cont+=1
        if cont == 30:
            break
    print("Se procesaron todas las páginas")
    print()
    print('------------------------------------------')


#-----------------------------------------------------------------------------------------------------------------------
# CONECTIVIDAD Y BASES DE DATOS
#-----------------------------------------------------------------------------------------------------------------------
# Para conectar con Mongo
# Regresa una conexión con la base mongo
def dbMongo_connection():
    ca = certifi.where()
    stringConnMongo = None
    try:
        stringConnMongo = MongoClient("mongodb+srv://admin:d10bWGsGGZByJuUw@cluster0.hd2zdo3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
    except Exception as error:
        print(error)
    return stringConnMongo

#Para conectar con Autonomous Database
# Regresa una conexión con la base oracle
def dbOracle_connection():
    cs='''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=g25fe25c70e5806_ic4302_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''
    conn = None
    try:
        conn = oracledb.connect(
                                user="ADMIN",
                                password="thisiswrongNereo08",
                                dsn=cs
                                )
    except Exception as error:
        print(error)
    return conn

# Esta función ingresa a la base AUTONOMOUS y revisa que archivos ya han sido procesados
# Regresa una lista con los nombres de cada uno de los archivos
def getFilesSQL():
    conn = dbOracle_connection()
    cursor = conn.cursor()
    s = cursor.var(oracledb.CURSOR)
    cursor.callproc('GET_FILENAMES', [s])
    data = s.getvalue().fetchall()
    data = [t[0] for t in data]
    return data

# Esta función ingresa a la base MONGO y revisa que archivos ya han sido procesados
# Regresa una lista con los nombres de cada uno de los archivos
def getFilesMongo():
    conn = dbMongo_connection()
    db = conn["Wikipedia"]
    collection = db["Files"]
    namelist = []
    for doc in collection.find():
        namelist.append(doc["Filename"])
    return namelist

# Función para Ingresar los datos de un archivo en la colección mongo
# En Mongo la colección de archivos consiste solamente en documentos con los nombres de cada uno
# Se recibe un diccionario que contiene el nombre del archivo
# Se ingresa este nombre a la colección
def insertarFileMongo(page_data):
    conn = dbMongo_connection()
    db = conn["Wikipedia"]
    collection = db["Files"]
    collection.insert_one(page_data)
    conn.close()

# Insertar los datos de una página a la colección mongo
# Aqui se inserta el diccionario con los datos procesados de un page
# Este diccionaro tendrá la estructura del diccionario generado por la funcion procees_page()
def insertarPageMongo(datos):

    # Se agregan número de links y hasredirection al documento

    datos['LinkNumber'] = len(datos['Links'])
    if datos['LastRevisionData']['Redirect'] != None:
        datos['LastRevisionData']['hasRedirect'] = "True"
    else:
        datos['LastRevisionData']['hasRedirect'] = "False"

    # Para las votaciones también se agrega un atributo rating, comienza como 0
    datos['Rating'] = 0

    # El atributo date se cambia de string a datetime
    datos['LastRevisionData']['RevisionDate'] = datetime.strptime(datos['LastRevisionData']['RevisionDate'], "%Y-%m-%dT%H:%M:%SZ")

    # Se conecta y se inserta todo el documento
    client = dbMongo_connection()
    db = client["Wikipedia"]
    collection = db["Pages"]

    # Insert data
    collection.insert_one(datos)

    # Close connection
    client.close()

# Función para ingresar los datos de un archivo a la base SQL
# Recibe los datos de un archivo, nombre, dbname, sitename, language
# Crea una instancia en la tabla file con el nombre dado
# Crea una instancia en la tabla site con el resto de datos, pone el id del file como fk
# Regresa el id del site para poder ligarlo con páginas
def insertFileSQL(filedata):
    conn = dbOracle_connection()
    cursor = conn.cursor()
    file_id = cursor.var(oracledb.NUMBER)
    cursor.callproc('INSERT_FILE', [filedata['Filename'], file_id])
    file_id = int(file_id.getvalue())
    conn.commit()

    site_id = cursor.var(oracledb.NUMBER)
    cursor.callproc('INSERT_SITE', [file_id,filedata['FileData']['dbName'],filedata['FileData']['siteName'],
                                    filedata['FileData']['Language'],site_id])

    site_id = int(site_id.getvalue())
    conn.commit()
    cursor.close()
    conn.close()
    return site_id

# Para insertar los datos de un page a las tablas de la base autonomous
# Se recibe el diccionario de datos, se asigna en variables y se llama al procedimiento INSERT_PAGE_ALL, INSERT_LINK e INSERT_Restriction
# Este se encarga de ingresar cada dato en sus respectivas tablas
def insertarPageSQL(page_data, siteId):

    pageid = page_data["PageId"]
    pagetitle = page_data["Title"]
    namespace = page_data["Namespace"]
    namespace = str(namespace)
    # Links es una lista
    links = page_data['Links']
    wikilink = page_data['WikipediaLink']
    generated = page_data['WikipediaGenerated']
    # Restrictions es una lista
    restrictions = page_data['Restrictions']
    # Revision User
    user_name = page_data['LastRevisionData']['User']['username']
    revision_text = page_data['LastRevisionData']['Text']['wikiText']
    clean_text = page_data['LastRevisionData']['Text']['NormalText']
    redirect = page_data['LastRevisionData']['Redirect']
    page_bytes = page_data['LastRevisionData']['PageBytes']
    revision_date = page_data['LastRevisionData']['RevisionDate']
    revision_datetime = datetime.strptime(revision_date, "%Y-%m-%dT%H:%M:%SZ")
    revision_date = oracledb.Date(revision_datetime.year, revision_datetime.month, revision_datetime.day)

    conn = dbOracle_connection()
    cursor = conn.cursor()

    try:
        # Call procedure
        cursor.callproc('INSERT_PAGE_ALL', [
            pageid,
            siteId,
            namespace,
            wikilink,
            pagetitle,
            generated,
            user_name,
            revision_text,
            redirect,
            page_bytes,
            revision_date,
            clean_text
        ])
        conn.commit()

        # Para guardar todos los datos de los links de las páginas
        for link in links:
            cursor.callproc('INSERT_LINK', [link,pageid])
            conn.commit()

        for restriction in restrictions:
            cursor.callproc('INSERT_RESTRICTION', [restriction,pageid])
            conn.commit()

    except:
        print("ERROR INGRESANDO PÁGINA")
        print(sys.exc_info()[1])
    cursor.close()
    conn.close()

#-----------------------------------------------------------------------------------------------------------------------
# FUNCIONES DATALOADER
#-----------------------------------------------------------------------------------------------------------------------
# Función comparar archivos en el bucket con archivos en las bases
# Avisa si solo una o ambas bases tienen un archivo, también si ninguna
# Recibe la lista de archivos para las bases y para el bucket

# Si SQL no lo tiene regresa el nombre del archivo y 'SQL'
# Si MONGO no lo tiene regresa el nombre del archivo y 'MONGO'
# Si AMBOS no lo tienen regresa el nombre del archivo y 'AMBOS'
# Sino retorna none
def VerificarArchivosProcesados(filesMongo, filesSQL, filesBucket):

    for file in filesBucket:
        if file in filesMongo and file not in filesSQL:
            return [file, 'SQL']

        elif file not in filesMongo and file in filesSQL:
            return [file, 'MONGO']

        elif file not in filesMongo and file not in filesSQL:
            return [file,'AMBOS']

        # Si no hay ningun archivo que insertar, se regresa none
        else:
            return None

# Función dataloader, la que se va a ejecutar cada cierto tiempo
def dataLoader():

    # Se va a repetir infinito
    while True:

        # Se conecta al bucket
        object_storage = connect_Bucket()
        print("Conectado con object storage")

        # Se obtiene la lista de archivos del bucket
        objetos_bucket = get_files_in_bucket(object_storage, "ic4302")
        print("Se obtuvieron los files del bucket")

        print("Revisando si hay archivos nuevos...")
        # Verificar si algún archivo no ha sido procesado:
        resultado = VerificarArchivosProcesados(getFilesMongo(), getFilesSQL(), get_bucket_objNames(objetos_bucket))

        if resultado == None:
            print('No se detectaron archivos nuevos')

        # Si se detecta un archivo nuevo
        else:
            nombre_archivo = resultado[0]
            base = resultado[1]
            print("Se detecto un archivo nuevo para " + base + ".")

            # Se descarga ese archivo
            file = downloadFile(object_storage, "ic4302", nombre_archivo)

            print("El archivo a procesar es ---> " + nombre_archivo)

            # Se procesa e ingresa a las bases
            process_file(file, base, nombre_archivo)

            os.remove(file)

        print()
        # Se espera 30 segundos antes de revisar de nuevo si hay un archivo a procesar
        time.sleep(30)

if __name__ == '__main__':
    dataLoader()



