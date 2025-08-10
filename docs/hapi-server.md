# What is the HAPI FHIR JPA Server?
<img src="images/hapi.png" alt="HAPI Logo" style="height:1in; float:left; margin-right:15px; margin-bottom:10px;" align="left" />
<a href = "(https://hapifhir.io">HAPI FHIR</a> is an open-source implementation of the HL7 FHIR specification developed by the University Health Network (UHN) in Toronto, Canada. It provides a mature, standards-based foundation for building FHIR-compliant solutions and has become one of the most widely used reference implementations in both research and healthcare innovation. HAPI FHIR supports RESTful APIs and integrates seamlessly with widely recognized terminologies such as SNOMED CT, LOINC, and ICD-10, ensuring that both structural and semantic interoperability can be achieved in line with HL7 standards. The <a href = "https://hapifhir.io/hapi-fhir/docs/server_jpa/get_started.html">HAPI FHIR JPA Server</a> extends the core HAPI FHIR library into a complete server solution that not only supports all core CRUD operations (create, read, update, delete) but also offers advanced capabilities for validation, terminology management, and International Patient Summary (IPS) generation using the <a href = "https://smilecdr.com/docs/ig_support/ips.html">$summary</a> operation.
<br clear="left"/>
<br>

# What is Docker?
<img src="images/docker.svg" alt="Docker Logo" style="height:1in; float:left; margin-right:15px; margin-bottom:10px;" align="left" />
<a href = "">Docker</a> is a platform that uses containerization to package and run applications. For the purpose of this project, Docker was used to run a HAPI FHIR JPA Server locally on a Microsoft Surface 3 Laptop running Windows 11 Home. The Docker image of HAPI FHIR is a pre-packaged version of a FHIR server that you can run using Docker to easily test, store, and manage healthcare data using the HL7 FHIR standard. Detailed instructions on running the Docker image of the HAPI FHIR JPA Server can be found on the <a href = "https://github.com/hapifhir">HAPI FHIR GitHub repository</a>.
<br clear="left"/>
<br>

# Interacting with the HAPI FHIR Server through Docker
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
<br>

## Useful Links
### YouTube Videos
- [DevDays (2021) Let's Build a FHIR App: Introduction HAPI Library for FHIR](https://youtu.be/nYPi2q_Tpks?si=WT9jqSkok0noNvYn)
- [Setting up a local HAPI FHIR Server for testing via Docker (Gino Canessa)](https://www.youtube.com/watch?v=EaJpJ0aQjiM)
- [HAPI FHIR Local Test Server (Gino Canessa)](https://youtu.be/EaJpJ0aQjiM?si=5XVxj2O9C9kALtwE)
- [James Agnew - Generating International Patient Summary with HAPI FHIR | DevDays 2024](https://youtu.be/ClGed65vLNk?si=3ZnNT29UScjcSZw8)
- [How to Set Up Your Own HAPI FHIR Server (Sidharth Ramesh)](https://youtu.be/M9mnj00hYlg?si=u2qpvGm2V182cEMy)
