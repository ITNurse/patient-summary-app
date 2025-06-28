# Using the HAPI FHIR Server


```bash
#Start a new HAPI FHIR server container in Docker, with the name hapi-fhir, using the hapiproject/hapi:latest image.
#Also mounts the hapi_data volume to the server's database directory
docker run -d -p 8080:8080 --name hapi-fhir -v hapi_data:/hapi-fhir-jpaserver-start/db hapiproject/hapi:latest #run HAPI 

#To restart the server
docker ps #Check running containers
docker rm hapi-fhir #if hapi-fhir container is already running, stop it
docker volume rm hapi-data #Erases all saved FHIR data

# Start HAPI FHIR Docker Container with Custom Config
# (Runs the HAPI FHIR container on port 8080, mounts application.yaml config, sets SPRING_CONFIG_LOCATION so that the config file is recognized)
docker run -d -p 8080:8080 --name hapi-fhir -v C:\Python\Wellness_Way\hapi-config:/configs -e SPRING_CONFIG_LOCATION=file:///configs/application.yaml hapiproject/hapi:latest

```