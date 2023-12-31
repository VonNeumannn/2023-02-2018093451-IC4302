from flask import Flask, jsonify, request
from flask_cors import CORS
import oracledb
from pymongo import MongoClient
from borneo import NoSQLHandle, NoSQLHandleConfig, PutRequest
from borneo.iam import SignatureProvider
import hashlib
import json
import datetime
from datetime import datetime
import certifi
import oci
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


#Constants
app = Flask(__name__)
# Configura CORS para toda la aplicación
CORS(app, resources={r"/*": {"origins": "*"}})

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
        return(error)
    return conn
#Mongo connection
def dbMongo_connection():
    ca = certifi.where()
    try:
        stringConnMongo = MongoClient("mongodb+srv://admin:d10bWGsGGZByJuUw@cluster0.hd2zdo3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
        db = stringConnMongo["Wikipedia"]
    except Exception as error:
        return(error)
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

#Firebase authentication
def firebaseConnection():
    # Use a service account.
    cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "registeruserswikisearch",
    "private_key_id": "24739b478e485bf606c432cb09875f8a9da7f228",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC0reiL/oI7Nh6f\nOOSm3CfOG6LMrBFrP4f8h1X/TbLUQspYr1ycXVya/u/cYu/K5yc51vQ8BU2dDO3z\nJG64vUtsK3CXDl9QWWhFcalgKsEijEKZF2ppMDZvZxtQ+atbscAjWJuEGIVL8Oq+\nYRfwICtl+8EzhmVo/PT8BF8E4XJWdsvfrFyrlonUH4GZ5FYa2eg3dzqzyLKEoVJR\nCgbF690TDM3ki9P17WrQac4mKbla9JwrYqiq+o2IUS1v3K0XpUxi4ERM5rPACxb+\nEaV7NNBpshT8Xt4AmEWEUVYON/mdgLhC/d81NG4rUKplbM9W14mcXXtliPS+1yvQ\nXjBHny6PAgMBAAECggEAE8Ae946utcJIvqb9d7ABOeqTdUQp80tSlixFHk9kCQf0\nDpW8zer2wIq1taWrCMcT5qK0uArsXQqYyEdnQxKOOBjXieusR6A+Ybj3BugljJ1A\nenOw0ibPDIZ82fEw5ikcE8EP3vS/PXnsbzs13q3lkJRgnj1GwJ9GOHZR3Lq4QPM0\nVeTx0FByzP6DtHw5JTCQxVcGpc/M2O4q+k3w3kMN6CgLeIJS6YWo3jXuPEVaMGQY\nMRPwyeYuJhDReXn2Fao9xtsDVV2Q+6AD3WvZbP63VlRjVHaF49JuDJ3MIvUdSREC\nixdWEPVe9aFH0BXP/f7H4mEOaGddiv/3TaQ0AxfjgQKBgQDoI8PtSFBPYvD0Xsj7\nSzYySs77/QIWA1oL6tAadD52rMoYP+2+TzI/6ur307ezgytQofLW695SoD3QYkH6\nM252PntmWj7u8kGVCEohvFB8L9HQL1xwhHz8co9Gh1YosqVYkibFMDkkS1h0/vbt\nNg4LvghLWmbrPYXcpBbTivNUcQKBgQDHQBQvKgTLeLXjUIzJ0pR9QNqzv9YYsOle\nZVX348L6OXObdz4NOTiUrKZFl1sQpNG1IBZqxCZgfXtLiGhB/BKxgtjagP0Ep3HD\nOx0sz1MX3oyXY1AZ7QPretJ4s5Oe9FoHo1ZGLSq/HmymjrXqkXcXxSRrBjWxXxoN\npoHoRMAy/wKBgG8RDaDtxF73O8nvv8FbzuZpHHc8Kk9V8zNYeZDupSQqr9bCX4F6\natRiFWHVjkL5MzQ1B/cEiy6FNI4LNP38tZEle+0QqKOyjOY9PRq++tMwHfa5ckTz\nXsl6FkrsXbDDKJEj/CDEXdKbqgrwIjyEbFv55AYJjsxmdzGF4NX92UZBAoGAEhJF\nwmFVPf8cwBk2K7flr9aJ/3OOv36MK/uU6H7H2FoNmjQedKST9SgTjIxFviS0wHDA\nl75inK3E2PzuN83dBCyR7n90c0+cidB6vO2w46FTrwda5H8Ss/DX1gqzgN84qyit\nUoAWOG9R+2lGJpg67PT8cJiHlibB/irz7VUO+ZECgYA98YtPEHV7lz2B1Nxgqbte\nQAbY0nmrzoAjuxxxjbECVZbYnUbcdqQpFEZgzCz8EWj2xYNHXvOL85gRHJYLhF+C\nGX3sx/WzTWsUdOOCrCSTVulM6/OHK+vjKmcu4lLdi9UQ9TSGHa6CVx6nO5uMvxGg\nXwrNdOefONHlk9hWoisl7Q==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-zytht@registeruserswikisearch.iam.gserviceaccount.com",
    "client_id": "110211652575937651143",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-zytht%40registeruserswikisearch.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }
    )
    # Genera una conexion a firestore
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
connFire = firebaseConnection()

#Register
@app.route("/register", methods=['POST'])
def register():
    date_time = datetime.now()
    timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    title = ""
    if request.method == 'POST':
        jsonCred = request.get_json()
        name = jsonCred["name"]
        lastName = jsonCred["lastName"]
        email = jsonCred["email"]
        password = jsonCred["password"]

        #agrega un nuevo documento a la coleccion usuarios
        connFire.collection("users").add({
            "name" : f"{name}",
            "lastName" : f"{lastName}",
            "email" : f"{email}",
            "password" : f"{password}"
        })
        title = f"Register: {name}"
        dbLogs(title,timeStamp)
        return jsonify({"message":"Registrado existosamente",
                        "status":1}), 201

#Login
@app.route("/login", methods=['POST'])
def login():
    date_time = datetime.now()
    timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    title = ""
    if request.method == 'POST':
        jsonCred = request.get_json()
        email = jsonCred["email"]
        password = jsonCred["password"]
        # Create a reference to the cities collection
        users = connFire.collection("users")
        # Create a query against the collection
        # Obtiene el documento que contenga el correo indicado 
        docs = (
            users
            .where(filter=FieldFilter("email", "==", f"{email}"))
            .stream()
        )
        user = None
        for doc in docs:
            user = doc.to_dict()
            
        try:
            if (user == None):
                title = "User no encontrado"
                dbLogs(title,timeStamp)
                return jsonify({"message":"Usuario no encontrado",
                            "status": 0}), 404
            else:
                if (user['password'] == password):
                    title = f"Login de: {user}"
                    dbLogs(title,timeStamp)
                    return jsonify({"message":f"{user['name']},logueado existosamente",
                                    "status":1})
                else:
                    title = "Correo o contraseña incorrecta"
                    dbLogs(title,timeStamp)
                    return jsonify({"message":f"Correo o contraseña incorrecta",
                                "status":0})
        except Exception as e:
            title = f"Error: {str(e)}"
            dbLogs(title,timeStamp)
            return e

#Search
@app.route("/search", methods=['GET'])
def search():
    #Se obtienen los parametros
    tipoRecurso = request.args.get('tipoRecurso')
    #Comprobamos el tipo de DB
    if (int(tipoRecurso) == 1):
        stringBusqueda = request.args.get('stringBusqueda')
        #Autonomous DB
        conn = dbOracle_connection()
        cursor = conn.cursor()
        #Log
        date_time = datetime.now()
        timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
        try:
        #Request
            sql = f"""
            SELECT
                LR."RevisionCleanText",
                P."Title"
            FROM
                "ADMIN"."LastRevision" LR
                INNER JOIN "ADMIN"."Page" P
                ON LR."PageId" = P."Pageid"
                INNER JOIN "ADMIN"."Site" S
                ON P."Siteid" = S."Siteid"
            WHERE
                CONTAINS(LR."RevisionCleanText", '%{stringBusqueda}%', 1) > 0
                OR CONTAINS(LR."Redirect", '%{stringBusqueda}%', 2) > 0
                OR CONTAINS(P."Namespace", '%{stringBusqueda}%', 3) > 0
                OR CONTAINS(P."WikipediaLink", '%{stringBusqueda}%', 4) > 0
                OR CONTAINS(P."Title", '%{stringBusqueda}%', 5) > 0
                OR CONTAINS(P."WikipediaGenerated", '%{stringBusqueda}%', 6) > 0
                OR CONTAINS(S."siteName", '%{stringBusqueda}%', 7) > 0
                OR CONTAINS(S."Language", '%{stringBusqueda}%', 8) > 0
                """
            cursor.execute(sql)
            rows = cursor.fetchall()
            pages = []
            for r in rows:
                clobText = r[0].read()
                result_dict = {
                'cleanText': clobText[:500],
                'title': r[1]
                }
                pages.append(result_dict)
            if len(pages) != 0:
                title = "Search exitoso"
                dbLogs(title,timeStamp)
                return jsonify(pages), 200
            else:
                title = "Search fallido"
                dbLogs(title,timeStamp)
                return "Not found", 404
        except Exception as e:
            title = f"Error: {str(e)}"
            dbLogs(title,timeStamp)
            return(f"Error: {str(e)}")
        finally:
            conn.close()
    else:
        stringBusqueda = request.args.get('stringBusqueda')
        #facetsParams = eval(request.args.get('facets'))
        facetsParams = []
        #facetsParams = [{"nombre": "NumberLinks", "valor": 50}]
        #facetsParams = []
        #Mongo DB
        conn = dbMongo_connection()
        collection = conn["Pages"]
        #logs
        date_time = datetime.now()
        timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
        title = ""
        try:
            #Busqueda general

            query = [{"$search":{
                "index":"full_text",
                "text":{
                    "path":["Title",
                            "LastRevisionData.Text.NormalText",
                            "LastRevisionData.User.username",
                            "LastRevisionData.Redirect",
                            "Restrictions",
                            "Links",
                            "FileData.dbName",
                            "FileData.siteName",
                            "FileData.Language"
                            ],
                    "query": stringBusqueda
                },
                "highlight":{
                    "path":"LastRevisionData.Text.NormalText"
                },
                "count":{
                    "type": "total"
                }
            }
            },
            {
              "$project": {
                "_id": 0,
                "Title": 1,
                "score": { "$meta": "searchScore" },
                "highlights": { "$meta": "searchHighlights" }
                }
            }
            ]
            queryFacets = ([
    {
        "$searchMeta": {
            "index": "full_text",
            "facet": {
                "operator": {
                    "compound": {
                        "should": [
                            {
                            "text": {
                                "query": [
                                    stringBusqueda
                                ],
                                "path": 
                                    ["Title",
                                    "LastRevisionData.Text.NormalText",
                                    "LastRevisionData.User.username",
                                    "LastRevisionData.Redirect",
                                    "Restrictions",
                                    "Links",
                                    "FileData.dbName",
                                    "FileData.siteName",
                                    "FileData.Language"
                                ]
                                }
                            }
                        ]
                    }
                },
                "facets": {
                    "LastRevisionData.PageBytes": {
                        "type": "number",
                        "path": "LastRevisionData.PageBytes",
                        "boundaries": [0, 100, 1000, 10000,1000000, 10000000],
                        "default": "otros"
                    },
                    "LastRevisionData.hasRedirect": {
                        "type": "string",
                        "path": "LastRevisionData.hasRedirect"
                    },
                    "LastRevisionData.RevisionDate": {
                        "type": "date",
                        "path": "LastRevisionData.RevisionDate",
                        "boundaries": [datetime.strptime("2000-01-01T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
                        datetime.strptime("2005-01-01T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
                        datetime.strptime("2015-01-01T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
                        datetime.strptime("2024-01-01T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")],
                        "default": "otros"
                    },
                    "LastRevisionData.User.username": {
                        "type": "string",
                        "path": "LastRevisionData.User.username"
                    },
                    "Namespace": {
                        "type": "string",
                        "path": "Namespace",
                        "numBuckets": 4
                    },
                    "LinkNumber": {
                        "type": "number",
                        "path": "LinkNumber",
                        "boundaries": [0, 10, 50, 100, 1000],

                    },
                    "Restrictions": {
                        "type": "string",
                        "path": "Restrictions",
                        "numBuckets": 4
                    },
                    "FileData.dbName": {
                        "type": "string",
                        "path": "FileData.dbName"
                    },
                    "FileData.Language": {
                        "type": "string",
                        "path": "FileData.Language"
                    },
                    "SiteName": {
                        "type": "string",
                        "path": "FileData.siteName"
                    },
                    "WikipediaLink": {
                        "type": "string",
                        "path": "WikipediaLink"
                    }
                }
            }
        },
    }])
            
            if len(facetsParams) == 0:
                resultsGeneral = list(collection.aggregate(query))
                resultsFacets= list(collection.aggregate(queryFacets))
                pages = []
                facets = []

                for doc in resultsGeneral:
                    pages.append(doc)
                for facet in resultsFacets:
                    facets.append(facet)

                if len(pages) != 0:
                    title = "Search exitoso"
                    dbLogs(title,timeStamp)
                    return [pages,facets], 200 #AQUI debería enviar los facets tambien
                else:
                    title + "Search fallido"
                    dbLogs(title,timeStamp)
                    return "Not found", 404
            else:

                query2 = [{
                        "$search": {
                        "index":"full_text",
                        "text":{
                            "path":["Title",
                                    "LastRevisionData.Text.NormalText",
                                    "LastRevisionData.User.username",
                                    "LastRevisionData.Redirect",
                                    "Restrictions",
                                    "Links",
                                    "FileData.dbName",
                                    "FileData.siteName",
                                    "FileData.Language"
                                    ],
                            "query": "this"
                        },
                        "highlight":{
                            "path":"LastRevisionData.Text.NormalText"
                        },
                        "count":{
                            "type": "total"
                        }
                        },
                        
                    },
                    {
                    "$match": {
                        "LastRevisionData.hasRedirect": "True"
                    }
                    },
                    {
                    "$project": {
                        "_id": 0,
                        "Title": 1,
                        "score": { "$meta": "searchScore" },
                        "highlights": { "$meta": "searchHighlights" }
                        }
                        }
                    ]
                resultWithFacets = list(collection.aggregate(query2))
                return resultWithFacets, 200
        except Exception as e:
            title = f"Error: {str(e)}"
            dbLogs(title,timeStamp)
            return(f"Error: {str(e)}")

#See Document
@app.route("/document", methods=['GET'])
def showDocument():
    #Obtiene los parametros
    titleDoc = request.args.get('title')
    tipoRecurso = request.args.get('tipoRecurso')
    #logs
    date_time = datetime.now()
    timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    title = ""
    #Comprueba el tipo de DB
    if (int(tipoRecurso) == 1):
        #Autonomous DB
        conn = dbOracle_connection()
        cursor = conn.cursor()
        #Request
        try:
            sql = f"""SELECT LR."RevisionCleanText",
                            P."WikipediaLink",
                            P."Rating"
                        FROM ADMIN."Page" P
                        INNER JOIN ADMIN."LastRevision" LR
                        ON LR."PageId" = P."Pageid"
                        WHERE P."Title" = '{titleDoc}'
                        """
            cursor.execute(sql)
            rows = cursor.fetchall()
            document = []
            for r in rows:
                clobText = r[0].read()
                result_dict = {
                'cleanText': clobText,
                'wikiLink': r[1],
                'rating': r[2]
                }
                document.append(result_dict)
            # Si el documento existe, devuelvo un json con el documento
            if document is not None:
                title = "Search exitoso"
                dbLogs(title,timeStamp)
                return jsonify(document), 200
            else:
                title = "Search fallido"
                dbLogs(title,timeStamp)
                return "Not found", 404
        except Exception as e:
            title = f"Error: {str(e)}"
            dbLogs(title,timeStamp)
            return(f"Error: {str(e)}")
        finally:
            conn.close()
    else:
        #Mongo DB
        conn = dbMongo_connection()
        collection = conn["Pages"]
        #logs
        date_time = datetime.now()
        timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
        title = ""
        try:
            results = collection.find_one({"Title":titleDoc})
            #results = list(collection.find(queryOne))
            wikiText = results.get("LastRevisionData", {}).get("Text", {}).get("NormalText")
            wikiLink = results.get("WikipediaLink")
            ratings = results.get("Rating")

            jsonWiki = {"wikiText":wikiText,
                        "wikiLink":wikiLink,
                        "rating":ratings}
            # Si el documento existe, devuelvo un json con el documento    
            if wikiText is not None:
                title = "Muestra el documento"
                dbLogs(title,timeStamp)
                return jsonify(jsonWiki), 200
            else:
                title = "No muestra el documento"
                dbLogs(title,timeStamp)
                return "Not found", 404
        except Exception as e:
            title = f"Error: {str(e)}"
            dbLogs(title,timeStamp)
            return(f"Error: {str(e)}")
        
@app.route("/rating", methods=['GET'])
def rateDoc():
    #Obtiene los parametros
    titleDoc = request.args.get('title')
    rating = int(request.args.get('rating'))
    #Log data
    date_time = datetime.now()
    timeStamp = date_time.strftime("%Y-%m-%dT%H:%M:%S")
    title = ""

    # oracle
    #connOracle = dbOracle_connection()
    #cursor = connOracle.cursor()
    # mongo
    connMongo = dbMongo_connection()
    collection = connMongo["Pages"]
    try:
        updateRating = f"""UPDATE "ADMIN"."Page"
                            SET "Rating" = NVL("Rating", 0) + {rating}
                            WHERE "Page"."Title" = '{titleDoc}'
                            """
        # Si el rating es distinto de 0, se actualiza el rating
        if rating != 0:
            #oracle
            #cursor.execute(updateRating)
            #connOracle.commit()
            #mongo
            collection.update_one({ "Title": titleDoc }, { "$inc": { "Rating": + rating } })
            title = f"Rate: {titleDoc} +- {rating} "
            dbLogs(title,timeStamp)
            return "Rating actualizado", 200
        else:
            return "Rating no actualizado", 200
    except Exception as e:
        return(f"Error: {str(e)}")
    finally:
        pass
        #connOracle.close()
# Main
if __name__ == '__main__':
    app.run()