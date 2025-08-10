# Pan-Canadian Patient Summary (PS-CA)

The [Pan-Canadian Patient Summary (PS-CA)](https://www.infoway-inforoute.ca/en/featured-initiatives/patient-summary) is a standardized extract of a patient’s health record designed to support continuity of care across borders and healthcare settings. It is based on the International Patient Summary (IPS) standard, and adapts this global framework to the Canadian context by incorporating national terminologies and jurisdiction-specific workflows. It enables clinicians to access essential health information—such as medications, allergies, and health concerns—without needing to navigate multiple systems or sift through unstructured notes. It supports both scheduled and unscheduled care, and is designed to be usable across diverse technical environments, including legacy systems and modern FHIR-based platforms.

![Screenshot of IPS composition showing required sections as: Header (subject, author, attester, custodian), Medication Summary, Allergies & Intolerances, and Problem List](images/ips-composition.png)
(Image Source: https://build.fhir.org/ig/HL7/fhir-ips/Structure-of-the-International-Patient-Summary.html)

## Learn More
#### YouTube
- [Connected Care: The Power of the Patient Summary](https://youtu.be/LXLj0ElsRNg?si=D8Q_G8KvZu4vgfu6)
- [What Connected Care Means to the Future of Canada's Health Care System](https://youtu.be/XoqzMAULasg?si=yuLXjGBJvAWEVZ8i)
- [DevDays (2024):  Moving to "Real" International Patient Summary (IPS) Implementations (Robert Hausam)](https://youtu.be/I86G6PyoVrg?si=_v1ChxnK1lovMWea)
- [IHE North America (2024): The International Patient Summary: A Worldwide Initiative](https://youtu.be/HKmmZQTK6BU?si=FrcU6xVTF7AhaRLD)
- [IHE Europe (2023): The Pan Canadian Patient Summary](https://youtu.be/YLsvI5GUc30?si=PUktY4Y5YWXuH-Cz)
- [Infoway Partnership Conference (2023): Demonstrating the Value of a Patient Summary](https://www.youtube.com/watch?v=s4sfMFB56mI&list=PLD40L51Q1YDhQMuduy9XJSnSG7s0vHOWD)
- [IHE Europe (2022): International Patient Summary, IHE and HL7 FHIR checks and balances (Grahame Grieve)](https://youtu.be/WvHgDbpNQ8c?si=LMgCwwTX7ZzHx5Pf)
- [DevDays (2022):  International Patient Summary: examples, tooling and exchange (Matt Rahn)](https://www.youtube.com/watch?v=s4sfMFB56mI&list=PLD40L51Q1YDhQMuduy9XJSnSG7s0vHOWD)
- [International Patient Summary: A-Z of FHIR (Chris Royale)](https://youtu.be/zK9DEpo66vs?si=bwtymS_tgjadybEs)
- [DevDays (2021):  International Patient Summary - Moving from Specification to Implementation (Robert Hausam)](https://youtu.be/efp7gn7DB30?si=8ltfyoMkBqrSiIfO)
- [DevDays (2019):  International Patient Summary (Rob Hausam)](https://www.youtube.com/watch?v=s4sfMFB56mI&list=PLD40L51Q1YDhQMuduy9XJSnSG7s0vHOWD)
- [International Patient Summary Proof of Concept](https://youtu.be/zpPlZNSvSB0?si=wiV-bhER2Levv4DA)

<br>

# Interoperability

Interoperability is foundational to the PS-CA. According to the [Health Information Management Systems Society (HIMSS)](https://legacy.himss.org/resources/interoperability-healthcare), it encompasses the ability of systems to access, exchange, integrate, and cooperatively use data across organizational and national boundaries. 

![Graphic displaying the levels of interoperability](images/interoperability.jpg)
(Image Source: Adebesin, F., Foster, R., Kotzé, P., & Van Greunen, D. (2013). A Review of Interoperability Standards in E-health and Imperatives for their Adoption in Africa. South African Computer Journal, 50. https://doi.org/10.18489/sacj.v50i1.176)

The PS-CA supports:

- Technical interoperability: Systems can connect and transmit data.
- Structural interoperability: Data follows consistent formats, such as HL7 FHIR.
- Semantic interoperability: Shared terminologies ensure consistent meaning.

## Learn More
#### YouTube
- [Connected Care. A Healthier Canada. Powered By Interoperability](https://youtu.be/A93_7N99HmY?si=n1fXUyWTd6cM3vk2)
- [Pan Canadian Health Data Strategy Presentation (2023)](https://youtu.be/VAqCDZS3QuA?si=-6Lj12-SuxUtBiyW)

<br>

# Health Information Exchange Standards

The PS-CA is built on a suite of health information exchange standards that define how data is structured, transmitted, and interpreted:

- [ISO 27269](https://www.iso.org/standard/79491.html): Defines the abstract model for the IPS.
- [HL7 FHIR](https://infocentral.infoway-inforoute.ca/en/standards/canadian/fhir): A modern, web-based standard for health data exchange.
- [IHE Profiles](https://www.ihe.net/news/ihe-releases-the-international-patient-summary-ips-profile/): Define real-world workflows, actors, and transactions for IPS exchange.

Canada Health Infoway’s [PS-CA Interoperability Specification](https://infoscribe.infoway-inforoute.ca/display/PSCAV1TI/ImplementationGuide) supports both FHIR and CDA formats, promoting broad adoption across provinces and territories.

<br>

# Controlled Terminology Standards

Terminologies and value sets ensure that exchanged data is meaningful and consistently interpreted. The PS-CA uses:

- [SNOMED CT Canadian Edition](https://accelero.infoway-inforoute.ca/en/standards/terminology-standards/snomed-ct-snomed-ct-ca): For clinical concepts.
- [pan-Canadian LOINC Observation Code Database (pCLOCD)](https://accelero.infoway-inforoute.ca/en/standards/terminology-standards/pclocd): For lab and observation data.
- [Canadian Clinical Drug Data Set (CCDD)](https://accelero.infoway-inforoute.ca/en/standards/terminology-standards/canadian-clinical-drug-data-set): For medication data.

These terminologies are maintained by Canada Health Infoway and distributed via the [Canadian Standards Release Centre](https://accelero.infoway-inforoute.ca/en/standards/terminology-standards) and [Terminology Gateway](https://tgateway.infoway-inforoute.ca/). Value sets are curated subsets of these terminologies, and data elements in the PS-CA are bound to them with varying levels of strictness (e.g., required, preferred, example, etc.).

## Learn More
#### Websites
[Connected Care Terminology Standards](https://accelero.infoway-inforoute.ca/en/standards/terminology-standards)
#### YouTube
- [Terminology Standards (Canada Health Infoway)](https://youtu.be/ZGX5oNKSUfA?si=LWQxXNCKqz6LGTaX)
- [Enhancing Terminology in the International Patient Summary (Rob Hausam](https://youtu.be/zcgo6DRQApA?si=OxeSZLSfbpvkyJHc)
- [International Patient Summary (IPS) adoption and implementation with SNOMED CT](https://youtu.be/O2HTepV6hGg?si=ocJVp-9OG4n0J10d)

<br>

# FHIR

FHIR (Fast Healthcare Interoperability Resources) is the preferred format for PS-CA implementation. It structures data into modular resources—such as Patient, Condition, and MedicationStatement—and supports exchange via standard web protocols.

The PS-CA FHIR Implementation Guide defines:

- Required and optional data elements.
- Terminology bindings.
- Profiles and extensions.
- Composition structure for the summary.

FHIR enables flexible, scalable, and interoperable patient summary exchange, and is supported by open-source tools like the HAPI FHIR JPA Server.

### Learn More
- [FHIR for Developers (Gino Canessa)](https://youtu.be/m2O6HiA1Z7g?si=lHAKkAHSBkKcstSg)
- [DevDays (2018) - Python FHIR Library (Ilya Beda)](https://youtu.be/dBAhIoArh80?si=i9-YyLWUtU07y7Ur)
- [PyTexas (2023) - An Introduction to FHIR and Python (Aly Sivji)](https://youtu.be/atWzjajDzBE?si=UEWlHNlylIejXFv1)
- [What is FHIR? - Resources, Profiles and FHIR Paradigms Explained (Sidharth Ramesh)](https://youtu.be/CtpkvtbgXE8?si=2eZacSRBt8HCjL-M)
- [How to create a FHIR resource in Python (Sidharth Ramesh)](https://youtu.be/jTiLXxyBYBY?si=jB8QZrIB71d9veXu)
- [Using Python to interact with FHIR REST APIs (Sidharth Ramesh)](https://youtu.be/iYB1iTohuyk?si=OeUtk1B2epQPEFbY)