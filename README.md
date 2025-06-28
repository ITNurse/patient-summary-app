# Patient Summary App

This project generates and validates HL7 FHIR-based patient summaries.

## Features
- Creates FHIR Patient Summary Bundles
- Validates bundles against HL7 implementation guides
- Includes sample synthetic patient data

## Requirements
- Python 3.x
- Docker (for running HAPI FHIR server)
- Python packages listed in `requirements.txt`

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ITNurse/patient-summary-app.git
cd patient-summary-app
```

### 2. Set up your Python environment

It’s recommended to use a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate   # On macOS/Linux

pip install -r requirements.txt
```

### 3. Install Docker (if you haven’t already)

Docker is required to run the HAPI FHIR server locally.

- Download and install Docker Desktop from:  
  [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

- After installing, make sure Docker is **running** in the background.  
  Look for the whale 🐳 icon in your system tray (Windows/macOS).

### 4. Start the HAPI FHIR server (via Docker)

```bash
docker run -d -p 8080:8080 hapiproject/hapi:latest
```

> Or use your own `application.yaml` configuration (instructions coming soon).

### 5. Run the application

```bash
python main.py
```

### 6. Output

FHIR Bundles will be created in the `document_bundles/` folder and POSTed to the FHIR server.

### 7. Open and Refresh the Power BI Report

The Power BI report file is located in the `powerbi/` folder.

To open and refresh the report:

1. Open `powerbi/patient-summary-report.pbix` in Power BI Desktop.
2. Click **Refresh** to load data directly from your running FHIR server.
3. If prompted, select **Web** as the data source type and ensure the FHIR server (e.g., `http://localhost:8080/fhir`) is running.

> **Note:** Some fields (e.g., `identifier`) may not appear correctly if you're connecting to a summary endpoint. Connect directly to each resource endpoint for full access.

## License
MIT

# Learn More

- [What is FHIR?](docs/fhir-overview.md)
- [IPS and PS-CA Implementation Guide](docs/ips-and-psca.md)
- [CSV File Design Decisions](docs/csv-design.md)
- [Terminology & Value Set Encoding](docs/value-sets.md)
- [Using the HAPI FHIR Server](docs/hapi-server.md)
- [How the Python App Works](docs/python-pipeline.md)
- [Using Power Query and Power BI](docs/power-query-bi.md)

