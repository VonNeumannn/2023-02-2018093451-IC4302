import unittest
import main
from main import *


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
        invalid_bucket = 'nonexistentbucket'
        self.assertRaises(Exception, main.get_files_in_bucket, main.connect_Bucket(), invalid_bucket)

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
            self.assertEqual(type(result2), str)

if __name__ == '__main__':
    unittest.main()
