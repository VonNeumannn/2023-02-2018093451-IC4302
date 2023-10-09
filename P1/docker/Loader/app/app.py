import bz2
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
from oracledb import LOB
from datetime import datetime


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

# FUNCIONES DE CONEXIÓN A ORACLE
#-----------------------------------------------------------------------------------------------------------------------
# Function to connect to the Oracle bucket
def connect_Bucket():
    oci.config.validate_config(config)
    object_storage = oci.object_storage.ObjectStorageClient(config)
    print("Connected to the object storage")
    return object_storage

# This function returns a list of all the object names in the bucket
# This is useful to check if a new file has been uploaded and needs to be processed
def get_files_in_bucket(object_storage,bucket_name):
    namespace = object_storage.get_namespace().data # The OCI namespace for your tenancy

    list_objects_response = object_storage.list_objects(namespace, bucket_name)
    objects = list_objects_response.data.objects

    return objects

def get_bucket_objNames(objectlist):
    names = []
    for obj in objectlist:
        names.append(obj.name)

    return names

# This function receives an object name
# and downloads it from the bucket to decompress it
# returns the downloaded file
def downloadFile(object_storage, bucket_name, object_name):
    namespace = object_storage.get_namespace().data
    obj = object_storage.get_object(namespace, bucket_name, object_name)

    # Write object bytes to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(obj.data.content)
    temp_file.close()

    return temp_file.name

# Function to decompress a bz2 file
# It receives a bz2 file, and decompresses it into a binary file
# Returns the decompressed binary file
def decompress_file(input_file):
    with bz2.open(input_file, 'rb') as f_in:
        return f_in.read()

#-----------------------------------------------------------------------------------------------------------------------
# Para Parsear texto y procesar las wikipages del documento
def get_last_revision(page):
    last_rev = None

    for revision in page:
        # Each iteration is a page revision
        last_rev = revision

    return last_rev

def parse_text(wiki_text):
    parsed = mwparserfromhell.parse(wiki_text)

    # Strip wiki markup, keep only plain text
    plain_text = parsed.strip_code(normalize=True, collapse=True)

    return plain_text

def get_links(text):

    parsed = mwparserfromhell.parse(text)

    links = []

    # Find all wikilinks
    for link in parsed.filter_wikilinks():
        # Get link target page title
        title = link.title.strip()

        # Generate full URL
        url = f'https://en.wikipedia.org/wiki/{title}'

        links.append(url)

    return links

def process_page(page):

  page_data = {}

  # Page metadata
  page_data["Title"] = page.title
  page_data["PageId"] = page.id
  page_data["Namespace"] = page.namespace

  # Get last revision
  last_revision = get_last_revision(page)

  # Last revision data
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

  # Other page data
  page_data['Restrictions'] = page.restrictions
  page_data['Links'] = get_links(last_revision.text)

  page_data['WikipediaLink'] = f'https://en.wikipedia.org/wiki/{page.title}'

  page_data['WikipediaGenerated'] = f'http://en.wikipedia.org/?curid={page.id}'

  return page_data

def process_file(file_obj, opcionAlmacenamiento, filename):
    # Decompress entire file
    binary_data = decompress_file(file_obj)
    # Convert binary chunk to BytesIO
    bytes_io = BytesIO(binary_data)

    # Pass to mwxml
    dump = mwxml.Dump.from_file(bytes_io)
    filename_Dat = {"Filename": filename}
    filename_Dat['FileData'] = {'dbName': dump.site_info.dbname, 'siteName': dump.site_info.name, 'Language': "English"}
    SQLsiteID = None
    if opcionAlmacenamiento == "SQL":
        SQLsiteID = insertFileSQL(filename_Dat)

    elif opcionAlmacenamiento == 'MONGO':
        insertarFileMongo(filename_Dat)

    else:
        SQLsiteID = insertFileSQL(filename_Dat)
        insertarFileMongo(filename_Dat)

    print(SQLsiteID)
    for page in dump:
        processed = process_page(page)
        processed['FileData'] = {'dbName': dump.site_info.dbname, 'siteName': dump.site_info.name, 'Language': "English" }

        print()
        print()
        print('------------------------------------------')
        print(processed)
        if opcionAlmacenamiento == 'AMBOS':
            insertarPageMongo(processed)
            insertarPageSQL(processed, SQLsiteID)

        elif opcionAlmacenamiento == "SQL":
            insertarPageSQL(processed, SQLsiteID)

        elif opcionAlmacenamiento == 'MONGO':
            insertarPageMongo(processed)

    print("Se procesaron todas las páginas")


#-----------------------------------------------------------------------------------------------------------------------
# CONECTIVIDAD Y BASES DE DATOS
# Para conectar con Mongo
def dbMongo_connection():
    ca = certifi.where()
    stringConnMongo = None
    try:
        stringConnMongo = MongoClient("mongodb+srv://admin:d10bWGsGGZByJuUw@cluster0.hd2zdo3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
    except Exception as error:
        print(error)
    return stringConnMongo

#Para conectar con Autonomous Database
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

def getFilesSQL():
    conn = dbOracle_connection()
    cursor = conn.cursor()
    s = cursor.var(oracledb.CURSOR)
    cursor.callproc('GET_FILENAMES', [s])
    data = s.getvalue().fetchall()
    data = [t[0] for t in data]
    return data


def getFilesMongo():
    conn = dbMongo_connection()
    db = conn["Wikipedia"]
    collection = db["Files"]
    namelist = []
    for doc in collection.find():
        namelist.append(doc["Filename"])
    return namelist

# Ingresar los datos de un archivo en la colección mongo
def insertarFileMongo(page_data):
    conn = dbMongo_connection()
    db = conn["Wikipedia"]
    collection = db["Files"]
    collection.insert_one(page_data)
    conn.close()

# Insertar los datos de una página a la colección mongo
def insertarPageMongo(datos):

    client = dbMongo_connection()
    db = client["Wikipedia"]
    collection = db["Pages"]

    # Insert data
    collection.insert_one(datos)

    # Close connection
    client.close()

# Para ingresar los datos de un archivo a la base SQL
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
def insertarPageSQL(page_data, siteId):

    pageid = page_data["PageId"]
    pagetitle = page_data["Title"]
    namespace = page_data["Namespace"]
    namespace = str(namespace)
    # assume links is a list
    links = page_data['Links']
    wikilink = page_data['WikipediaLink']
    generated = page_data['WikipediaGenerated']
    # assume restrictions is a list
    restrictions = page_data['Restrictions']
    # Revision User
    user_id = page_data['LastRevisionData']['User']['UserID']
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

    # DATE
    typeObj = conn.gettype("STRING_VARRAY")
    linksVA = typeObj.newobject()
    restrictionsVA = typeObj.newobject()

    linksVA.extend(links)
    restrictionsVA.extend(restrictions)
    try:
        # Call procedure
        cursor.callproc('INSERT_PAGE_ALL', [
            pageid,
            siteId,
            namespace,
            wikilink,
            pagetitle,
            generated,
            user_id,
            user_name,
            revision_text,
            redirect,
            page_bytes,
            revision_date,
            clean_text,
            linksVA,
            restrictionsVA
        ])
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

#-------------------------------------------------------------------------------------------------------------------
# Función para ver si algún archivo del bucket no se ha insertado en alguna de las bases
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

# This function checks every 30 seconds if there is a new file in object storage,
# if that is the case it processes the XML data and stores it into MongoDB and Autonomous DB
# This function doesn't stop, it continuously runs in the background
def dataLoader():
    #while True:
    # Connect to the bucket
    object_storage = connect_Bucket()

    # Get the list of files in the bucket
    objetos_bucket = get_files_in_bucket(object_storage, "ic4302")
    print("Se obtuvieron los files del bucket")

    # Verificar si algún archivo no ha sido procesado:
    resultado = VerificarArchivosProcesados(getFilesMongo(), getFilesSQL(), get_bucket_objNames(objetos_bucket))

    if resultado == None:
        pass

    else:
        nombre_archivo = resultado[0]
        base = resultado[1]
        print("Se detecto un archivo nuevo para " + base + ". Se va a procesar:")

        file = downloadFile(object_storage, "ic4302", nombre_archivo)

        print("El archivo a procesar es ---> " + nombre_archivo)
        # Process the new file
        process_file(file, base, nombre_archivo)

        os.remove(file)

    # Wait for 30 seconds before checking for new files again
    time.sleep(30)


#dataLoader()
insertarPageSQL({'Title': 'AfghanistanHistory', 'PageId': 13, 'Namespace': 0, 'LastRevisionData': {'User': {'UserID': 9784415, 'username': 'Tom.Reding'}, 'Text': {'wikiText': '#REDIRECT [[History of Afghanistan]]\n\n{{Redirect category shell|1=\n{{R from CamelCase}}\n}}', 'NormalText': 'REDIRECT History of Afghanistan'}, 'PageBytes': 90, 'Redirect': 'History of Afghanistan', 'RevisionDate': '2017-06-05T04:18:18Z'}, 'Restrictions': [], 'Links': ['https://en.wikipedia.org/wiki/History of Afghanistan'], 'WikipediaLink': 'https://en.wikipedia.org/wiki/AfghanistanHistory', 'WikipediaGenerated': 'http://en.wikipedia.org/?curid=13', 'FileData': {'dbName': 'enwiki', 'siteName': 'Wikipedia', 'Language': 'English'}},0)
