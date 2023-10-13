import unittest
import requests
import os

baseurl = 'http://127.0.0.1:5000/'
email = 'joctan@estudiantec.cr'
name = 'Joctan'
lastname = 'Porras'
password = '12345'
busqueda = 'car'
rating = '0'
title = 'Anarchism'

class test_api(unittest.TestCase):
    def test_login(self):
        url = baseurl+'/login'
        credentials = {'email': email, 'password': password}
        response = requests.post(url,credentials)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def test_register(self):
        url = baseurl+'/register'
        data = { 'email': email,
                'name': name,
                'lastname': lastname,
                'password': password
                }
        response = requests.post(url,data)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def test_searchOracle(self):
        url = baseurl+ '/search?stringBusqueda='+busqueda+'&tipoRecurso=1'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def test_searchMongo(self):
        url = baseurl+ '/search?stringBusqueda='+busqueda+'&tipoRecurso=2'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def test_documentOracle(self):
        url = baseurl+ '/document?title='+title+'&tipoRecurso=1'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def test_documentMongo(self):
        url = baseurl+ '/document?title='+title+'&tipoRecurso=2'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def test_rating(self):
        url = baseurl+ '/rating?title='+title+'&tipoRecurso=1'+'&rating='+rating

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def test_rating(self):
        url = baseurl+ '/rating?title='+title+'&tipoRecurso=2'+'&rating='+rating

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)
        
if __name__=="__main__":
   unittest.main()