# Patient Summary App

This project generates and validates HL7 FHIR-based patient summaries.

## Features
- Creates FHIR Patient Summary Bundles
- Validates bundles against HL7 implementation guides
- Includes sample synthetic patient data

## Requirements
- Python 3.x
- Docker (for running HAPI FHIR server)
- [Any other dependencies]

## Getting Started

### 1. Clone the repository
git clone https://github.com/ITNurse/patient-summary-app.git
cd patient-summary-app

### 2. Set up your Python environment
It's recommended to use a virtual environment:
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On macOS/Linux
pip install -r requirements.txt
Note: Create a requirements.txt file listing required Python packages if you haven't already.

### 3. Start the HAPI FHIR server (via Docker)
docker run -d -p 8080:8080 hapiproject/hapi:latest
Or use your custom application.yaml if needed (instructions TBD).

### 4. Run the application
python main.py

### 5. Output
FHIR Bundles will be created in the document_bundles/ folder and POSTed to the FHIR server.

## License
MIT
