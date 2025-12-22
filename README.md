# Patient Summary App

This project generates synthetic HL7 FHIR-based patient summaries aligned with the Pan-Canadian Patient Summary (PS-CA) standard. It posts them to a HAPI FHIR server, which is used as the data source for a Patient Viewer dashboard built with Microsoft Power BI.

![GIF demo of Patient Viewer dashboard built with Microsoft Power BI](docs/images/Demo1.gif)

## Features
- Creates FHIR Patient Summary Bundles based on synthetic patient data aligned with PS-CA value sets
- Runs HAPI FHIR server image using Docker
- Posts bundles to HAPI FHIR server
- Connects to HAPI FHIR server using Power Query in Microsoft Power BI, unpacks .json into tables, and visualizes the data.

## Requirements
- Computer running Windows
- Git (If you are new to Git, check out [this YouTube video](https://www.youtube.com/watch?v=r8jQ9hVA2qs))
- Knowledge of how to work with the Command Prompt (If you are new to this, check out [this YouTube video](https://www.youtube.com/watch?v=QBWX_4ho8D4))
- Python 3.x
- Microsoft Power BI desktop

## Getting Started

### 1. Clone the repository

In Windows, open the Command Prompt application (you can search for it in your start menu)
In the command window that appears, enter the following command and press enter:
```bash
git clone https://github.com/ITNurse/patient-summary-app.git
```
Then enter the following command and press enter:
```bash
cd patient-summary-app
```

### 2. Set up your Python environment

In the command window, enter the following commands:

```bash
python -m venv venv
venv\Scripts\activate 

pip install -r requirements.txt
```

### 3. Install and run Docker

Docker is required to run the HAPI FHIR server locally.

- Download and install Docker Desktop from:  
  [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

- After installing, make sure Docker is **running** in the background.  
  Look for the whale 🐳 icon in your system tray (Windows/macOS).

- For more information on interacting with the FHIR server:
  [Interacting with the HAPI FHIR Server](docs/hapi-server.md)

### 4. Start the HAPI FHIR server (via Docker)

In the command window, enter the following command:

```bash
docker run -d -p 8080:8080 hapiproject/hapi:latest
```
Wait a couple of minutes for the server to start, then open a web browser and navigate to `http://localhost:8080/fhir` to ensure it is running. You should see something like this:

![Screenshot of HAPI FHIR server landing page](docs/images/hapi-fhir-localhost.jpg)


### 5. Run the application

In the command window, enter the following command:
```bash
python main.py
```
You should see the following output:

![Screenshot of command line output from running the application](docs/images/command_line.jpg)

### 6. Output

FHIR Bundles will be created in the `document_bundles/` folder. Check this folder and you should be able to see see the bundles. The resources should also have been POSTed to the FHIR server. Check the following links and you should be able to see them:
- [Composition Resources](http://localhost:8080/fhir/Composition)
- [Patient Resources](http://localhost:8080/fhir/Patient)
- [Medication Resources](http://localhost:8080/fhir/MedicationStatement)
- [Immunization Resources](http://localhost:8080/fhir/Immunization)
- [AllergyIntolerance Resources](http://localhost:8080/fhir/Patient)

### 7. Open and Refresh the Power BI Report

The Power BI report file is located in the `powerbi/` folder.

To open and refresh the report:

1. Open `powerbi/patient-summary-report.pbix` in Power BI Desktop.
2. Click **Refresh** to load data directly from your running FHIR server.
3. You should see the synthetic data from the csv files used to created the patient summaries.

### 8. Stop the FHIR server and delete the data

If you want to run the script more than once, it is necessary to stop the FHIR server and delete the data before you run it again. Otherwise duplicates will be created. To do this, run the following commands in the command prompt:

```bash
docker ps 
docker stop hapi-fhir #if hapi-fhir container is already running, stop it
docker rm hapi-fhir #remove hapi-fhir container
docker volume rm hapi_data #Erases all saved FHIR data
```


## License
MIT

# Future Work To Be Completed:
- Improve conformance validation: Explore HAPI FHIR server configuration to generate clearer validation feedback, making it easier to troubleshoot PS-CA compliance issues.
- Address Power BI limitations: Revisit licensing options or alternatives so the FHIR connector and online publishing can be used, reducing barriers for learners to access the dashboard.
- Enhance Python app logic: Add PUT operations to prevent duplicate resources and expand the synthetic dataset (Results, Devices, Vital Signs) to better reflect the PS-CA scope.
- Test with external data: Run the app against datasets like Synthea to validate adaptability and performance with more complex, realistic patient scenarios.
- Develop bilingual reporting: Build an English/French version of the Power BI report to reflect Canada’s official languages, investigating how to handle HL7 value sets available only in English.
- Expand documentation: Add terminology primers, Infoway resources, and SNOMED/LOINC guidance so new users have the context they need to learn and apply the standards.
- Recruit volunteer testers: Ask others to walk through the repo, flag unclear instructions, and try running the project, ensuring usability and accessibility for independent learners.

# Learn More

- [What is the Pan-Canadian Patient Summary?](docs/pan-canadian-patient-summary.md)
- [CSV File Design Decisions and Value Sets](docs/csv-design-and-value-sets.md)
- [Interacting with the HAPI FHIR Server](docs/hapi-server.md)
- [How the Python App Works](docs/python-pipeline.md)
- [Using Power Query and Power BI](docs/power-query-bi.md)



[def]: docs/images/command_line.jpg