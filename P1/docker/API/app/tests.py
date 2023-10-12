import unittest
import requests
import os

baseurl = 'http://127.0.0.1:5000/'
phrase = 'another'
artist = 'beyonce'
language = 'es'
genre = 'Pop'
minPop = '0'
maxPop = '100'
amountOfSongs = '10'
songName = 'robot.html'

class test_api(unittest.TestCase):
    def testLogin(self):
        url = baseurl+'/login'

        response = requests.post(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def testRegister(self):
        url = baseurl+'/register'

        response = requests.post(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def testSearchOracle(self):
        url = baseurl+ '/search?'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def testSearchMongo(self):
        url = baseurl+ '/search?'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def testDocumentOracle(self):
        url = baseurl+ '/document?'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)

    def testDocumentMongo(self):
        url = baseurl+ '/document'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        condition = ('Error' in response.json())
        self.assertEqual(condition, False)



if __name__=="__main__":
   unittest.main()