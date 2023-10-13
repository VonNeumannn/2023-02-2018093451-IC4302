sudo docker login
cd ..
cd docker

# Se crea la imagen para hacer la infrastructura
cd autonomousInfrastructure
sudo docker build -t vonneumannn/autonomous-infrastructure .
sudo docker images
sudo docker push vonneumannn/autonomous-infrastructure

# Se crea la imagen del componente Loader
cd ..
cd Loader
sudo docker build -t vonneumannn/wiki-loader .
sudo docker images
sudo docker push vonneumannn/wiki-loader

# Imagen para crear el API
cd .. 
cd API
sudo docker build -t vonneumannn/api-wikidb .
sudo docker images
sudo docker push vonneumannn/api-wikidb

# Imagen para crear el componente Web
cd ..
cd UI
sudo docker build -t vonneumannn/docker-react .
sudo docker images
sudo docker push vonneumannn/docker-react
