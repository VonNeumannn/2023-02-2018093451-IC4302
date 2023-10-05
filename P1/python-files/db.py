from flask import Flask, jsonify, request
import oracledb
from pymongo import MongoClient
import oci
from oci.nosql import NosqlClient
import sys
from borneo import NoSQLHandle, NoSQLHandleConfig, PutRequest
from borneo.iam import SignatureProvider
import hashlib
import json
import datetime
import certifi

#Constants
app = Flask(__name__)

"""
TODO:
-> Send data to UI
-> Insert into log DB
    #el bag_info va el json(log) completo, md5 a todo el doc para el logId
    #primera busqueda sin facets
    #iterativo por cada facet
    #mongo stage
"""
#Oracle connection
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
#Mongo connection
def dbMongo_connection():
    ca = certifi.where()
    try:
        stringConnMongo = MongoClient("mongodb+srv://admin:d10bWGsGGZByJuUw@cluster0.hd2zdo3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
        #stringConnMongo = MongoClient("mongodb+srv://admin:h99HYgct2cPpgVUwgaXruVY5V@cluster0.b5lzzny.mongodb.net/?retryWrites=true&w=majority")
        db = stringConnMongo["Wikipedia"]
    except Exception as error:
        print(error)
    return db

#Logs insertion
def dbLogs(title, timeStamp):
    private_key = """-----BEGIN PRIVATE KEY-----
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
-----END PRIVATE KEY-----"""
    user =  "ocid1.user.oc1..aaaaaaaashik7hmu6usm4tpruwrubbs6h6e5lyix6lcu67odiuc7vbfcvotq"
    fingerprint = "06:25:27:f2:e2:81:c8:f2:18:9e:8a:d1:65:8c:5b:4d"
    tenancy = "ocid1.tenancy.oc1..aaaaaaaaazrw3t5sa6dacgzzh573u763zxazhcnve2ndfdgaebwgh6dxlptq"
    region = "us-ashburn-1"

    provider = SignatureProvider(tenant_id=tenancy,
                                 user_id=user,
                                 fingerprint=fingerprint,
                                 private_key=private_key,
                                 pass_phrase=None)

    nosql_handle = NoSQLHandle(NoSQLHandleConfig(region,provider))
    #Definir lo que se va a insertar
    table_name = "ic4302_logs"
    log_entry = {
        "title":title,
        "timeStamp":timeStamp
        }
        
    #obtengo un valor único para el id
    encoded_entry = json.dumps(log_entry)
    hashed_entry = hashlib.md5(encoded_entry.encode()).hexdigest()
    final_log = {
        "logId":hashed_entry,
        "title":title,
        "bagInfo":log_entry,
        "timeStamp" : timeStamp}
    #Se realiza la insercion
    rq = PutRequest().set_table_name(table_name)
    rq.set_value(final_log)
    nosql_handle.put(rq)

#Search by title
@app.route("/search", methods=['GET'])
def search():
    #Se obtienen los parametros
    tipoRecurso = request.args.get('tipoRecurso')
    #Comprobamos el tipo de DB
    if (int(tipoRecurso) == 1):
        stringBusqueda = '%'+request.args.get('stringBusqueda')+'%'
        #Autonomous DB
        conn = dbOracle_connection()
        cursor = conn.cursor()
        #Log
        date_time = datetime.datetime.now()
        timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
        try:
        #Request
            sql = f"""EXEC ADMIN.BUSCAQUEDAGENERAL '{stringBusqueda}',0
                    """
            cursor.execute(sql)
            rows = cursor.fetchall()
            pages = []
            for r in rows:
                result_dict = {
                'IDPAGINA': r[0],
                'TITULO': r[1]
                }
                pages.append(result_dict)
            if len(pages) != 0:
                title + "Search exitoso"
                dbLogs(title,timeStamp)
                return jsonify(pages), 200
            else:
                title + "Search fallido"
                dbLogs(title,timeStamp)
                return "Not found", 404
        except Exception as e:
            return(f"Error: {str(e)}")
        finally:
            conn.close()
    else:
        stringBusqueda = request.args.get('stringBusqueda')
        #Mongo DB
        conn = dbMongo_connection()
        collection = conn["Pages"]
        #logs
        date_time = datetime.datetime.now()
        timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
        title = ""
        try:
            queryMongo = {
                        "$or": [
                            {"Title": {"$regex": stringBusqueda, "$options": "i"}},
                            {"LastRevisionData.Text.NormalText": {"$regex": stringBusqueda, "$options": "i"}},
                            {"Restrictions": {"$regex": stringBusqueda, "$options": "i"}},
                            {"Links": {"$elemMatch": {"$regex": stringBusqueda, "$options": "i"}}}
                        ]}
            #Busqueda por patrones
            documents = collection.find()
            pages = []
            i = 0
            for doc in documents:
                result_dict = {
                "Title": doc["Title"],
                "NormalText": doc["LastRevisionData"]["Text"]["NormalText"]
                }
                pages.append(result_dict)
                i+=1
            print(i)
            # Para obtener los facets
            """
            facetsSelected = ["Namespace", "Redirect", "PageHasRedirect", "Restrictions",
                            "SiteInfoName", "SiteInfoDBName", "SiteLaguage", "PageLastModified",
                            "PageLastModifiedUser",  "PageBytes", "PageNumberLinks"]
            facets = {}
            for select in facetsSelected:
                pipeline = [{"$match": queryMongo},  # Aplicar el mismo filtro de búsqueda
                            {"$group": {"_id": f"${select}", "count": {"$sum": 1}}}]
                resultFacets = list(collection.aggregate(pipeline))
                facets[select] = resultFacets
            """
            if len(pages) != 0:
                title + "Search exitoso"
                dbLogs(title,timeStamp)
                return jsonify(pages), 200 #AQUI debería enviar los facets tambien
            else:
                title + "Search fallido"
                dbLogs(title,timeStamp)
                return "Not found", 404
        except Exception as e:
            return(f"Error: {str(e)}")

#See Document
@app.route("/document", methods=['GET'])
def showDocument():
    #Obtiene los parametros
    idDocument = request.args.get('idDocument')
    tipoRecurso = request.args.get('tipoRecurso')
    #logs
    date_time = datetime.datetime.now()
    timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    title = ""
    #Comprueba el tipo de DB
    if (int(tipoRecurso) == 1):
        #Autonomous DB
        conn = dbOracle_connection()
        cursor = conn.cursor()
        #Request
        try:
            sql = f"""SELECT IDPAGINA, TITULO, NAMESPACE, REDIRECT, RESTRICTION 
                        FROM PAGINA
                        WHERE IDPAGINA = {idDocument}
                        """
            cursor.execute(sql)
            rows = cursor.fetchall()
            document = None
            for r in rows:
                document = r
            if document is not None:
                title + "Search exitoso"
                dbLogs(title,timeStamp)
                return jsonify(document), 200
            else:
                title + "Search fallido"
                dbLogs(title,timeStamp)
                return "Not found", 404
        except Exception as e:
            return(f"Error: {str(e)}")
        finally:
            conn.close()
    else:
        #Mongo DB
        conn = dbMongo_connection()
        collection = conn["PAGINA"]
        #logs
        date_time = datetime.datetime.now()
        timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
        title = ""
        try:
            #Muestra la pagina según el id
            documents = collection.find_one({"IDPAGINA":idDocument})
            print(documents)
            page = None
            for doc in documents:
                page = doc
            if page is not None:
                title + "Search exitoso"
                dbLogs(title,timeStamp)
                return jsonify(page), 200
            else:
                title + "Search fallido"
                dbLogs(title,timeStamp)
                return "Not found", 404
        except Exception as e:
            return(f"Error: {str(e)}")

# Main
if __name__ == '__main__':
    app.run()
