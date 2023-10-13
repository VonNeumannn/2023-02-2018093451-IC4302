import unittest
import requests
import os
import app
from app import *


class test_api(unittest.TestCase):
    def setUp(self):
        app.app_context().push()
   #def test_oracleConnection(self):
   #    # Llamada a la función de conexión
   #    conn = dbOracle_connection()
   #    # Si se conecta
   #    self.assertEqual(conn, "Conexión exitosa")
   #    # Si no se conecta
   #    self.assertNotEqual(conn, "Conexión fallida")
   #    # Cerrar conexión
   #    conn.close()

    def test_mongoConnection(self):
        # Llamada a la función de conexión
        conn = dbMongo_connection()
        # Si se conecta
        self.assertIsNotNone(conn, "Conexión exitosa")
        
    #def test_login(self):
    #    url = 'http://127.0.0.1:5000'+'/login'
    #    credentials = {"email": "joctan@estudiantec.cr",
    #                    "password": "12345"}
    #    response = requests.post(url,credentials)
    #    self.assertEqual(response.status_code, 200)
#
    #    print(response.json()) # Imprime la respuesta de la solicitud HTTP
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    #def test_register(self):
    #    url = 'http://127.0.0.1:5000'+'/register'
    #    data = { 'email': "pedro",
    #            'name': "jpedro@gmail.com",
    #            'lastname': "Acuña",
    #            'password': "Chavez"
    #            }
    #    response = requests.post(url,data)
    #    self.assertEqual(response.status_code, 200)
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    #def test_searchOracle(self):
    #    busqueda = 'Ejemplo'
    #    url = 'http://127.0.0.1:5000'+ '/search?stringBusqueda='+busqueda+'&tipoRecurso=1'
#
    #    response = requests.get(url)
    #    self.assertEqual(response.status_code, 200)
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    def test_searchMongo(self):
        busqueda = 'Ejemplo'
        url = 'http://127.0.0.1:5000'+ '/search?stringBusqueda='+busqueda+'&tipoRecurso=2'
        conn = dbMongo_connection()
        collection = conn["Pages"]
        
        data2Insert = {
            "Title": "Ejemplo",
            "PageId": 1,
            "Namespace": "Ejemplo",
            "FileData": {
                "dbName": "DB1",
                "siteName": "Site1",
                "Language": "English"
            },
            "LastRevisionData": {
                "User": {
                    "UserID": 123,
                    "username": "Usuario1"
                },
                "Text": {
                    "wikiText": "Texto1",
                    "NormalText": "Texto normal1"
                },
                "PageBytes": 1024,
                "Redirect": None,
                "RevisionDate": "2023-10-13"
            },
            "Restrictions": ["Restricción1", "Restricción2"],
            "Links": ["Link1", "Link2"],
            "WikipediaLink": "EnlaceWiki1",
            "WikipediaGenerated": "Generado1"
        }
        collection.insert_one(data2Insert)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

        collection.delete_one(data2Insert)

    #def test_documentOracle(self):
    #    title = 'Ejemplo'
    #    url = 'http://127.0.0.1:5000'+ '/document?title='+title+'&tipoRecurso=1'
    #
    #    response = requests.get(url)
    #    self.assertEqual(response.status_code, 200)
    #
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)  

    def test_documentMongo(self):
        title = 'Ejemplo'
        url = 'http://127.0.0.1:5000'+ '/document?title='+title+'&tipoRecurso=2'
        conn = dbMongo_connection()
        collection = conn["Pages"]
        
        data2Insert = {
            "Title": "Ejemplo",
            "PageId": 1,
            "Namespace": "Ejemplo",
            "FileData": {
                "dbName": "DB1",
                "siteName": "Site1",
                "Language": "English"
            },
            "LastRevisionData": {
                "User": {
                    "UserID": 123,
                    "username": "Usuario1"
                },
                "Text": {
                    "wikiText": "Texto1",
                    "NormalText": "Texto normal1"
                },
                "PageBytes": 1024,
                "Redirect": None,
                "RevisionDate": "2023-10-13"
            },
            "Restrictions": ["Restricción1", "Restricción2"],
            "Links": ["Link1", "Link2"],
            "WikipediaLink": "EnlaceWiki1",
            "WikipediaGenerated": "Generado1",
            "Rating": 0
        }

        collection.insert_one(data2Insert)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

        collection.delete_one(data2Insert)

    #def test_ratingOracle(self):
    #    title = 'Ejemplo'
    #    rating = 1
    #    url = 'http://127.0.0.1:5000'+ '/rating?title='+title+'&tipoRecurso=1'+'&rating='+rating
##
    #    response = requests.get(url)
    #    self.assertEqual(response.status_code, 200)
##
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    #def test_ratingMongo(self):
    #    title = 'Ejemplo'
    #    rating = '0'
    #    url = 'http://127.0.0.1:5000'+ '/rating?title='+title+'&tipoRecurso=2'+'&rating='+rating
    #    conn = dbMongo_connection()
    #    collection = conn["Pages"]
#
    #    #Query para insertar documento
    #    data2Insert = {
    #        "Title": "Ejemplo",
    #        "PageId": 1,
    #        "Namespace": "Ejemplo",
    #        "FileData": {
    #            "dbName": "DB1",
    #            "siteName": "Site1",
    #            "Language": "English"
    #        },
    #        "LastRevisionData": {
    #            "User": {
    #                "UserID": 123,
    #                "username": "Usuario1"
    #            },
    #            "Text": {
    #                "wikiText": "Texto1",
    #                "NormalText": "Texto normal1"
    #            },
    #            "PageBytes": 1024,
    #            "Redirect": None,
    #            "RevisionDate": "2023-10-13"
    #        },
    #        "Restrictions": ["Restricción1", "Restricción2"],
    #        "Links": ["Link1", "Link2"],
    #        "WikipediaLink": "EnlaceWiki1",
    #        "WikipediaGenerated": "Generado1",
    #        "Rating": 0
    #    }
    #    response = requests.get(url)
    #    self.assertEqual(response.status_code, 200)
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)
    #    
    #    collection.delete_one(data2Insert)

if __name__=="__main__":
   unittest.main()