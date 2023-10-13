import unittest
import app as main
from app import *

"""
class TestsBucket(unittest.TestCase):

    # Se prueba si se puede conectar correctamente con el bucket en la base
    def test_connect_bucket(self):

        #Para que la conexion sea exitosa se debe regresar un objeto de tipo <class 'oci.object_storage.object_storage_client.ObjectStorageClient'>
        result = main.connect_Bucket()
        expected_type = oci.object_storage.object_storage_client.ObjectStorageClient
        self.assertEqual(type(result),expected_type)
        self.assertNotEqual(type(result), None)

    # Para probar si se pueden sacar archivos del bucket
    def test_GetFiles(self):

        # Se busca que el resultado siempre se llame con el mismo nombre del bucket
        result = main.get_files_in_bucket(main.connect_Bucket(),'ic4302')

        # Supuestamanete se debe regresar una lista de datos
        self.assertEqual(type(result), list)

        # Se verifica que con otros nombres de bucket pasen errores
       # invalid_bucket = 'nonexistentbucket'
       # self.assertRaises(Exception, main.get_files_in_bucket, main.connect_Bucket(), invalid_bucket)

    # Probar obtener nombres de archivos en el bucket y descargar 1
    def test_get_bucket_file(self):

        result = main.get_bucket_objNames(main.get_files_in_bucket(main.connect_Bucket(),'ic4302'))

        # se debe regresar una lista de datos
        self.assertEqual(type(result), list)

        # La lista de datos debe ser vacia o sino se revisa si todos sus elementos son strings
        if result == []:
            pass
        else:
            for obj_name in result:
                self.assertTrue(type(obj_name) == str)

            # Probar descargando un archivo del bucket, solo funciona si se subio uno
            result2 = main.downloadFile(main.connect_Bucket(), "ic4302", result[0])

            # Se debería regresar el nombre de un archivo temporal

            # El archivo descargado debe ser
            self.assertEqual(type(result2), str, "No se logro descargar el archivo")

"""
class TestsConectividad(unittest.TestCase):

    # Definimos un método de prueba para la conexión MongoDB
    def test_Mongodbconn(self):
        # Se crea una conexión con Mongo
        connM = dbMongo_connection()

        # Verificamos que la conexión no sea None
        self.assertIsNotNone(connM, "La conexión con Mongo no se pudo lograr")

        # Se obtienen los nombres de las bases de datos en el cluster
        dbs = connM.list_database_names()

        # Si existe la base de datos Wikipedia todo bien
        self.assertIn('Wikipedia', dbs,"No se encontro la base de datos Wikipedia en Mongo")

        # Se cierra la conexión
        connM.close()

    def test_MongoGet(self):
        # Se prueba obteniendo los nombres de los archivos en la base
        files = getFilesMongo()

        # Se asegura que se haya regresado una lista, sea vacía o no
        self.assertIsInstance(files, list)

        # Guardamos la longitud inicial
        initial_count = len(files)

        # Para probar el insert se ingresa un File y luego se borra
        # P.S solo se prueba ingresar File y no Page, ya que por su estructura similar si funciona uno el otro también
        data = {"Filename": "test_file",
                "FileData": {"dbName": 'test', "siteName": "test", "Language": "English"}}

        insertarFileMongo(data)

        # Se obtienen los datos nuevamente
        files = getFilesMongo()

        # Se comprueba que ahora haya un archivo más
        self.assertEqual(len(files), initial_count + 1)

        # Se busca el archivo insertado
        self.assertIn("test_file", files)

        # Se borra el archivo insertado
        db = dbMongo_connection()
        collection = db["Wikipedia"]["Files"]
        collection.delete_one({"Filename": "test_file"})

        # Se comprueba que la cantidad vuelva a ser la inicial
        files = getFilesMongo()
        self.assertEqual(len(files), initial_count)

        db.close()

    """
    def test_oracle_connection(self):
        # Se crea una conexión con Autonomous SQL
        connS = dbOracle_connection()
        self.assertIsNotNone(connS, "No se pudo conectar a Oracle")
        connS.close()

    def test_oracleGet(self):
        # Se prueba el método para obtener archivos en la db
        files = getFilesSQL()

        # Se asegura que se haya regresado una lista, sea vacía o no
        self.assertIsInstance(files, list)

        # Guardamos la longitud inicial
        initial_count = len(files)

        data = {"Filename": "test_file",
                "FileData": {"dbName": 'test', "siteName": "test", "Language": "English"}}

        # Se va a insertar el file a los datos, esto no afecta nada, por lo tanto se deja en la base
        insertFileSQL(data)

        files = getFilesSQL()

        # Se comprueba que ahora haya un archivo más
        self.assertEqual(len(files), initial_count + 1)
    """

class TestVerificarDondeArchivo(unittest.TestCase):

    def test_verificarArchivos(self):

        # Se van a probar 4 casos, uno donde SQL no lo tenga, uno para Mongo y uno donde ambos ocupen
        # También se va a probar cuando ninguno de los dos ocupe el archivo

        # Caso 1 SQL
        output = main.VerificarArchivosProcesados(["Archivo1"], ["Archivo2"], ["Archivo1"])

        self.assertEqual(output[0], "Archivo1")
        self.assertEqual(output[1], 'SQL')

        # Caso 2 Mongo
        output = main.VerificarArchivosProcesados(["Archivo1"], ["Archivo2"], ["Archivo2"])

        self.assertEqual(output[0], "Archivo2")
        self.assertEqual(output[1], 'MONGO')

        # Caso 3 Ambos
        output = main.VerificarArchivosProcesados(["Archivo1"], ["Archivo2"], ["Archivo3"])

        self.assertEqual(output[0], "Archivo3")
        self.assertEqual(output[1], 'AMBOS')

        # Caso 4 Ninguno
        output = main.VerificarArchivosProcesados(["Archivo1"], ["Archivo1"], ["Archivo1"])

        self.assertIsNone(output)


# Para revisar las funciones de Parsing con mwParserFromHell
class TestParseFunctions(unittest.TestCase):

    # Parsear un texto de tipo Wikitext
    def test_parse_text(self):

        # Se define un wikitext
        wikitext = "[[File:Example.jpg|An example image]]\n\nSome text with a [[Link|display text]] and [[Another Link]]."

        # Se muestra como se debería ver parseado
        expected = "An example image\n\nSome text with a display text and Another Link."
        result = parse_text(wikitext)

        # Se comparan ambos para ver si el esperado y el resultado son iguales
        self.assertEqual(expected, result)

    # Para probar extraer los links del wikitext
    def test_get_links(self):

        # Se define el wikitext
        wikitext = "[[Link]] [[Another Link]] [[Link 3|Display]]"

        # Links esperados
        expected_links = [
            "https://en.wikipedia.org/wiki/Link",
            "https://en.wikipedia.org/wiki/Another Link",
            "https://en.wikipedia.org/wiki/Link 3"
        ]

        # Se obtienen los links
        links = get_links(wikitext)

        # Se comparan los obtenidos con los esperados
        self.assertEqual(expected_links, links)


if __name__ == '__main__':
    unittest.main()
