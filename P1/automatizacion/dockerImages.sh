sudo docker login
cd ..
cd docker
cd autonomousInfrastructure
sudo docker build -t jcardonar/autonomous-infrastructure .
sudo docker images
sudo docker push jcardonar/autonomous-infrastructure
