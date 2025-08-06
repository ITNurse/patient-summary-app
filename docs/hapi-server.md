## What is the HAPI FHIR JPA Server?
<img src="images/hapi.png" alt="HAPI Logo" style="height:1in; float:left; margin-right:10px;" />
<a href="https://hapifhir.io">HAPI FHIR</a> is an implementation of the HL7 FHIR specification for Java. The <a href="https://hapifhir.io/hapi-fhir/docs/server_jpa/get_started.html">HAPI FHIR JPA Server</a> is a fully contained FHIR server, supporting all standard operations (read/create/delete/etc.).
<div style="clear: both;"></div>

## What is Docker?
<img src="images/docker.svg" alt="Docker Logo" style="height:1in; float:left; margin-right:10px;" />
<a href="https://www.docker.com/">Docker</a> is a platform that uses containerization to package and run applications. For the purpose of this project, Docker was used to run a HAPI FHIR JPA Server locally on a Microsoft Surface 3 Laptop running Windows 11 Home.
The Docker image of HAPI FHIR is a pre-packaged version of a FHIR server that you can run using Docker to easily test, store, and manage healthcare data using the HL7 FHIR standard. Detailed instructions on running the Docker image of the HAPI FHIR JPA Server can be found on the <a href="https://github.com/hapifhir/hapi-fhir-jpaserver-starter">HAPI FHIR GitHub repository</a>.
<div style="clear: both;"></div>


## Interacting with the HAPI FHIR Server through Docker
### Running the HAPI FHIR Server
Start a new HAPI FHIR server container in Docker, with the name hapi-fhir, using the hapiproject/hapi:latest image.
Also mounts the hapi_data volume to the server's database directory
```bash
docker run -d -p 8080:8080 --name hapi-fhir -v hapi_data:/hapi-fhir-jpaserver-start/db hapiproject/hapi:latest 
```

### To check logs as server is starting
```bash
docker logs -f hapi-fhir
```

### To restart the server
```bash
docker ps 
docker stop hapi-fhir #if hapi-fhir container is already running, stop it
docker rm hapi-fhir #remove hapi-fhir container
docker volume rm hapi_data #Erases all saved FHIR data
```

### Start HAPI FHIR Docker Container with Custom Config
Runs the HAPI FHIR container on port 8080, mounts application.yaml config, sets SPRING_CONFIG_LOCATION so that the config file is recognized
```bash
docker run -d -p 8080:8080 --name hapi-fhir -v C:\Python\Wellness_Way\hapi-config:/configs -e SPRING_CONFIG_LOCATION=file:///configs/application.yaml hapiproject/hapi:latest
```