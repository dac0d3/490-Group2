# AstroCultivators

**Contributors:** Codi Yost, Neville Elieh, Sandra Davis

---
## Overview

AstroCultivators is an autonomous farming system designed to facilitate the growth of self-pollinating crops with minimal human intervention. By incorporating features such as autonomous monitoring, real-time data reporting, environment management, automatic harvesting, and cleaning, this system aims to streamline plant growth operations and reduce the need for manual labor.

---

![Headliner image](Headliner.png)
## Developer Tools
![nVIDIA](https://img.shields.io/badge/nVIDIA-%2376B900.svg?style=for-the-badge&logo=nVIDIA&logoColor=white)  <br> 
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)  <br>
![Apache](https://img.shields.io/badge/apache-%23D42029.svg?style=for-the-badge&logo=apache&logoColor=white)  <br>
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  <br>
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)  <br>
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)  <br>
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)  <br>

## Project Maintenence

- **Main**:
  - *Maintained by Neville Elieh*
  - For release or the newest version of the project.

- **Web Application**:
  - *Maintained by Sandra Davis*
  - Web interface for accessing and managing the system.

- **Sensor Data Code**:
  - *Maintained by Codi Yost*
  - Codebase responsible for collecting and processing sensor data.

--- 

## Repository Setup  
```+---.vscode
+---bme_sensor
|   \---Sensor_csv_data
+---Web Application
|   +---.idea
|   \---Front End
|       +---python scripts
|       \---Website
|           \---.vs
|               \---Website
|                   +---config
|                   +---FileContentIndex
|                   \---v17
\---WebApp_BackEnd
    \---astrocultivators_r1
        +---static
        |   \---Website
        |       \---.vs
        |           \---Website
        |               +---config
        |               +---FileContentIndex
        |               \---v17
        \---templates
```

---

## Version 2 of Web Application Frontend
*In Production*

To activate the virtual environment:

1. Navigate to the `Astrocultivator_Web_App` folder.
2. Run the following command:
.venv\Scripts\activate


To run the website in debug mode:

1. Navigate to the `Astrocultivator_Web_App` folder.
2. Run the following command:
python run.py

The website will run locally on port 5000. You can access it in any browser by typing:
localhost:5000

---
## Version 1 of Current Live Web Application

This folder contains files that are crucial for the backend server and the frontend display. Contains files including images and templates. Following must be implemented on the Jetson Orin because it is the host server for the web application.

1. Navigate to the `/AstroCultivators/WebApp_BackEnd/astrocultivators_r1` folder.
2. Run the following command:
   python astrocultivators_web.py

The website will be live on the web via the Jetson Orin's IP address.

---
## BME_Sensor
The contents of this folder pertains to all operations of the BME Sensor. Contains code on gathering sensor data, code that converts sensor data into a viewable CSV file (bound to change).

   1. Navigate to `BME_Sensor` folder.
        
   You will find python scripts for the sensor, sensor data, sample data, and notes.

## Live Demo of Version 1 of the Web Application
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/NAGFOsAXRy4/0.jpg)](https://www.youtube.com/watch?v=NAGFOsAXRy4)


