import unittest
import requests
import os
import app
from app import *

baseurl = 'http://127.0.0.1:5000/'
email = 'joctan@estudiantec.cr'
name = 'Joctan'
lastname = 'Porras'
password = '12345'
busqueda = 'car'
rating = '0'
title = 'Anarchism'

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
    #    url = baseurl+'/login'
    #    credentials = {"email": "joctan@estudiantec.cr",
    #                    "password": "12345"}
    #    response = requests.post(url,credentials)
    #    response.headers['Content-Type' ] = 'application/json'
    #    self.assertEqual(response.status_code, 200)
#
    #    print(response.json()) # Imprime la respuesta de la solicitud HTTP
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    #def test_register(self):
    #    url = baseurl+'/register'
    #    data = { 'email': email,
    #            'name': name,
    #            'lastname': lastname,
    #            'password': password
    #            }
    #    response = requests.post(url,data)
    #    self.assertEqual(response.status_code, 200)
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    #def test_searchOracle(self):
    #    url = baseurl+ '/search?stringBusqueda='+busqueda+'&tipoRecurso=1'
#
    #    response = requests.get(url)
    #    self.assertEqual(response.status_code, 200)
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    def test_searchMongo(self):
        url = baseurl+ '/search?stringBusqueda='+busqueda+'&tipoRecurso=2'
        conn = dbMongo_connection()
        collection = conn["Pages"]
        
        data2Insert = {
            "Title": "Ejemplo 1",
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

        conn.close()
        
    #def test_documentOracle(self):
    #    url = baseurl+ '/document?title='+title+'&tipoRecurso=1'
#
    #    response = requests.get(url)
    #    self.assertEqual(response.status_code, 200)
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    #def test_documentMongo(self):
    #    url = baseurl+ '/document?title='+title+'&tipoRecurso=2'
#
    #    response = requests.get(url)
    #    self.assertEqual(response.status_code, 200)
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    #def test_ratingOracle(self):
    #    url = baseurl+ '/rating?title='+title+'&tipoRecurso=1'+'&rating='+rating
#
    #    response = requests.get(url)
    #    self.assertEqual(response.status_code, 200)
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)

    #def test_ratingMongo(self):
    #    url = baseurl+ '/rating?title='+title+'&tipoRecurso=2'+'&rating='+rating
#
    #    response = requests.get(url)
    #    self.assertEqual(response.status_code, 200)
#
    #    condition = ('Error' in response.json())
    #    self.assertEqual(condition, False)
        
if __name__=="__main__":
   unittest.main()