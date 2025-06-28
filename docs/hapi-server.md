# Using the HAPI FHIR Server


```bash
docker ps #Check running containers
docker stop hapi-fhir #stop the container
docker rm hapi-fhir #remove the container
docker run -d -p 8080:8080 hapiproject/hapi:latest #run HAPI FHIR server

# Start HAPI FHIR Docker Container with Custom Config
# (Runs the HAPI FHIR container on port 8080, mounts application.yaml config, sets SPRING_CONFIG_LOCATION so that the config file is recognized)
docker run -d -p 8080:8080 --name hapi-fhir -v C:\Python\Wellness_Way\hapi-config:/configs -e SPRING_CONFIG_LOCATION=file:///configs/application.yaml hapiproject/hapi:latest

```