sudo docker login
cd ..
cd docker

# Se crea la imagen para hacer la infrastructura
cd autonomousInfrastructure
sudo docker build -t jcardonar/autonomous-infrastructure .
sudo docker images
sudo docker push jcardonar/autonomous-infrastructure

# Se crea la imagen del componente Loader
cd ..
cd Loader
sudo docker build -t jcardonar/wiki-loader .
sudo docker images
sudo docker push jcardonar/wiki-loader

# Imagen para crear el API
cd .. 
cd API
sudo docker build -t jcardonar/api-wikidb .
sudo docker images
sudo docker push jcardonar/api-wikidb

# Imagen para crear el componente Web
cd ..
cd UI
sudo docker build -t jcardonar/docker-react.
sudo docker images
sudo docker push jcardonar/docker-react
