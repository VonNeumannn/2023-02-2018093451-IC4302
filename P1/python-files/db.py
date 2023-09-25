from flask import Flask, jsonify, request
import oracledb
from pymongo import MongoClient
import oci
from oci.nosql import NosqlClient, models



#Constants
app = Flask(__name__)

"""
TODO:
-> Send data to UI
-> Insert into log DB
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
    try:
        stringConnMongo = MongoClient("mongodb+srv://admin:h99HYgct2cPpgVUwgaXruVY5V@cluster0.b5lzzny.mongodb.net/?retryWrites=true&w=majority")
        db = stringConnMongo["Wikipedia"]
    except Exception as error:
        print(error)
    return db
#Logs insertion
def dbLogs():
    config = {
    "key_content": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCohhfZRsLjgQug
p3IHTr7xX04nCVGrbWxsC2acv3ub57TmqduMqcpRyMM0TN0xRtE5hPxPs9UvXTRR
zz4pMogUlIZ2kYU6sLHHL/VVYypnkxmAJRiGvx3gxjLVIzaVZIqUoF17mcnW+G4q
YB6/fBWrF5WmxxcMbJJx7SL0+KufZ3ix2ezshIcJPjX4lzRMTriXpCpKPOdCmNiW
EXOfHg2L/LxlCFJA+Cqsoy97RXQYIDuw0LocmjV+JR3aFjMM+okV/LdbRr80sOTZ
unSlqaJX7VvC2i4+XCZ3GScX8FKLpjsJx6k2BTKwTG3fo5exXYsXGGqaKD+B1atT
DycAPvsDAgMBAAECggEAN1NahgL0nXLyqcn/JgYEqsJyql8lWEXCuA/gHqrAfnUJ
z0ZJZTsiyEnESCnJ3lEVBDC0EsiDvxp2wDrs+eJ0iWkfYdKxbgyvOKj2fpNhSwKg
dxD2pdodiXsYGiAG3fHViyjAuADLok8J/9Bxl8S5amOCRnALEZGdXFiRRuJSmbB5
lhIwprtuW10/zUfIu7RRtSrVacrgTmvfZyhZaFJdKFlkmMg+DsMg+hGqrke4RyNs
A2J5UYm/Iorc2aG21Ack3x7Hlkm9E/NWSQEwFKvAOyOKBNxLByUpth77MiPEGRk6
CXIEeP89Ggl0H13aBG8lz1lM+/lBUY3BEQYaVxqu+QKBgQDrv7PjHEOzl9NdW7Gu
38ZJtawjA39Me3/L1cHQmjF9udDNQ27rkKPpAZ9VB9AQybQXmV2kfNZUsBoWg++v
HkaN9t2SJsp8lJbEzHM7ABOk8P716m1aVJL7htjDrAyo5+o3YpS/rmu3bQf6G+4N
HK8ztxZzX0hmhJbGrxQZAPVKKQKBgQC3AA97dkPAfEFrfgf2ADQOgwNg58zEl1La
tMjTwMdZjML/L6Ec+mgF2jhhvIcdp6DX18+lSQNdrloKj6F/aH1MDqoUmZmdfcCc
WbItyq/mWCNoxgtYdMfXv1jIQkl5c+MZUWw0OMIbfsbNn5Lyt9a9SnJLaGsrHsZF
jLkmrApZSwKBgEIbAk032sAcXbd7A8r+krKOj9NNor+GjeJRcUSWSDRyC1vTgeHq
MBwhSVVlmHFsreRELB74pn0e2GHh4y7etXgPdjgKSpM+czyB+/naXqfMsCGy97Dx
sDl5qYTM1Mv0JBgdu4o4VZocp7T5afohRfuhZlk5qaqdmU3jQCZ2v1FpAoGBAJtU
DtAhmvJnxXOC3yj8FTN4GscHGXSIaQhASPILgGnPI7hMajlZhi/pgM/coOcX4Fs0
0AggSB4dHko2jcLCIxAKpmyjz5KxKWrMa4OYteMTTsLgzsJ/JR1ISgh40zqmlc1o
oipVPtTtr7raxnUEe93hsc+1yrkn/u0LvCBKCOKvAoGBALtGclEKdVkShoU/G82n
4yNi0q5pRuAshgFwb/eDJ8QoV3A26ABxY29MCNGb1Qcz9+CWrsGZQYblGBv+KCj+
HHo6gzP+wyVO8NqdInNy12Ueqgn37QrXoUdPHiFXoTj1VrTiW0ail9Zd3cspxOFZ
JNyOgHzvdQI78zC1tLUJETI1
-----END PRIVATE KEY-----""",
    "user": "ocid1.user.oc1..aaaaaaaashik7hmu6usm4tpruwrubbs6h6e5lyix6lcu67odiuc7vbfcvotq",
    "fingerprint": "8f:34:1c:92:df:13:5c:1b:f2:b2:b6:9f:75:27:9a:55",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaaazrw3t5sa6dacgzzh573u763zxazhcnve2ndfdgaebwgh6dxlptq",
    "region": "us-ashburn-1"
    }
    oci.config.validate_config(config)
    nosql_client = NosqlClient(config)
    log_entry = {
        "title":"prueba",
        "bagInfo":""
    }

    insert_request = nosql_client.put_row(
        table_name = "ic4302_logs",
        value = log_entry
    )
    return insert_request

#Queries
@app.route("/login", methods=['GET'])
def validarUser():
    pass

#Search by title
@app.route("/search", methods=['GET'])
def search():
    #Se obtienen los parametros
    stringBusqueda = '%'+request.args.get('stringBusqueda')+'%'
    tipoRecurso = request.args.get('tipoRecurso')
    dbLogs()
    #Comprobamos el tipo de DB
    if (int(tipoRecurso) == 1):
        #Autonomous DB
        conn = dbOracle_connection()
        cursor = conn.cursor()
        try:
        #Request
            sql = f"""SELECT P.IDPAGINA, P.TITULO
                    FROM PAGINA P
                    WHERE TITULO
                    LIKE '{stringBusqueda}'
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
                return jsonify(pages), 200
            else:
                return "Not found", 404
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            conn.close()
    else:
        #Mongo DB
        conn = dbMongo_connection()
        collection = conn["PAGINA"]
        try:
            #Busqueda por patrones
            documents = collection.find({"TITULO":{"$regex":stringBusqueda,"$options": "i"}})
            pages = []
            for doc in documents:
                result_dict = {
                'IDPAGINA': doc[1],
                'TITULO': doc[2]
                }
                pages.append(result_dict)
            if len(pages) != 0:
                return jsonify(pages), 200
            else:
                return "Not found", 404
        except Exception as e:
            print(f"Error: {str(e)}")

#See Document
@app.route("/document", methods=['GET'])
def showDocument():
    #Obtiene los parametros
    idDocument = request.args.get('idDocument')
    tipoRecurso = request.args.get('tipoRecurso')
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
                return jsonify(document), 200
            else:
                return "Not found", 404
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            conn.close()
    else:
        #Mongo DB
        conn = dbMongo_connection()
        collection = conn["PAGINA"]
        try:
            #Muestra la pagina según el id
            documents = collection.find_one({"IDPAGINA":idDocument})
            print(documents)
            page = None
            for doc in documents:
                page = doc
            if page is not None:
                return jsonify(page), 200
            else:
                return "Not found", 404
        except Exception as e:
            print(f"Error: {str(e)}")


# Main
if __name__ == '__main__':
    app.run()
