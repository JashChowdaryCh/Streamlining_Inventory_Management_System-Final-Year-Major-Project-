# Streamlining Inventory Management System with AI and IoT Technologies



## Table of Contents
- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Problem Statement (Existing System Limitations)](#problem-statement-existing-system-limitations)
- [Proposed System](#proposed-system)
- [Objectives](#objectives)
- [Scope](#scope)
- [Expected Outcomes](#expected-outcomes)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [System Architecture](#system-architecture)
- [Installation Guide](#installation-guide)
- [Usage](#usage)
- [Complexity Analysis](#complexity-analysis)
- [Team Members](#team-members)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Introduction
In today's fast-evolving mechanical landscape, efficient stock administration has become a cornerstone of operational success—especially in resource-intensive spaces like the material industry. Conventional stock systems often suffer from challenges such as manual errors, delayed stock updates, lack of real-time data, and inefficient asset allocation. These issues can lead to overstocking, stockouts, and significant financial losses. With the increasing demand for intelligent, automated, and data-driven systems, Artificial Intelligence (AI) and Internet of Things (IoT) technologies have emerged as powerful enablers of next-generation stock administration.

## Project Overview
The Stock Administration Framework developed in this project is a shrewd, AI-driven platform custom-made specifically for the material industry. It addresses critical challenges faced in traditional stock practices, such as inconsistent stock tracking, delayed decision-making, overstocking, understocking, and wastage of resources. It combines machine learning algorithms with virtually mimicked IoT sensors to bring insights, automation, and real-time monitoring into each stage of stock handling and manufacturing.

The core components of this project include stock monitoring, fabric demand forecasting, cost prediction, alternative product proposals, waste reusing proposals, and a fire discovery security module. Each feature is backed by dedicated AI models that are trained using industry-specific datasets, ensuring that forecasts and alerts are accurate and highly relevant. The framework enables stock managers to make proactive decisions by determining market demand and optimizing the capacity and acquirement of crude, in-process, and finished materials.

On the IoT side, the project employs Arduino Uno for virtual sensor reenactments. Apparatuses like Wokwi, ThingsBoard, and Ubidots are utilized to imitate real-time sensor information, which enhances the system's capacity to monitor environmental conditions such as temperature, stickiness (humidity), and smoke. These reenactments provide real-time cautions and proposals, such as moving textures sensitive to high mugginess or signaling potential fire hazards. This integration ensures that stock security and quality are maintained under changing environmental conditions, without the need for costly physical equipment.

The backend of the framework is developed using Python and Flask, where all the machine learning models and information processing logic dwell. The frontend is built using HTML, CSS, and JavaScript, offering a user-friendly interface for stock managers to interact with the system—viewing expectations, managing information, and responding to cautions. The application is designed to be modular, versatile, and intuitive, making it easy to adopt in medium to large-scale material operations. Overall, this project exhibits a cutting-edge approach to stock administration, leveraging the power of artificial intelligence and virtual IoT to enhance operational productivity, diminish misfortunes, ensure security, and support sustainable practices. It is not only cost-effective but also scalable for use in other manufacturing segments beyond textiles, opening doors for future developments and integration.

## Problem Statement (Existing System Limitations)
Conventional stock administration frameworks in the textile industry are often manual or semi-automated, heavily relying on human oversight and experience. These systems typically involve physically recording stock levels, product movement, and orders using spreadsheets or basic software without intelligent analytics. As a result, they are prone to errors, delays, and inefficiencies. Managers confront challenges in predicting demand trends accurately, leading to either overstocking or stockouts, both of which have financial implications. There is also limited integration with real-time natural monitoring or caution frameworks, which makes it difficult to ensure sensitive materials like textures that can corrupt under unacceptable capacity conditions. Besides, cost adjustments are ordinarily reactive, based on obsolete data, and seldom consider market trends or competitor estimating dynamically.

Another key impediment of the existing framework is the need for AI-driven insights for alternative manufacturing proposals or squander reusing. Most of the squander generated in material production is either disposed of or repurposed without a structured decision-making model. Moreover, while some businesses have embraced fundamental IoT sensors, they often lack centralized dashboards, caution components, or integration with AI-driven choice back frameworks. The failure to automate decisions like restocking alarms, request surges, or natural dangers causes delays and increments reliance on manual intervention. There is also no shrewd component in place to recommend texture choices or reusing procedures based on real-time or prescient analytics.

## Proposed System
The proposed framework presents an intelligent and integrated stock administration solution enhanced with Artificial Intelligence and Virtual IoT innovations, particularly custom-tailored for the material industry. The framework aims to automate and optimize stock handling, demand estimating, cost prediction, squander reusing, and security monitoring using a combination of backend AI models and virtual hardware reenactments through platforms like Wokwi. It leverages machine learning algorithms such as Linear Regression, Arbitrary Timberland (Random Forest), and LSTM to anticipate demand and cost patterns based on historical data. This allows stock supervisors to proactively manage stock.

A critical advancement within the proposed framework is the usage of Virtual IoT technologies utilizing Arduino Uno reenactments rather than genuine sensors due to budget and time imperatives. These virtual sensors monitor environmental parameters such as temperature and mugginess (humidity) to secure textures from harm. For instance, if the mugginess level surpasses a secure limit, the system will trigger alerts.

The framework is built using Flask (Python) for backend processing and HTML/CSS/JavaScript for the frontend, offering an intelligent web application interface. It provides dashboards for stock availability, predictive analytics, and suggestions. With highlights like real-time demand alerts, fabric protection based on environmental variables, and sustainable squander administration, the proposed framework significantly enhances operational efficiency, reduces manual workload, and supports data-driven decision-making.

## Objectives
The primary objective of this project is to develop an intelligent and integrated Stock Administration Framework that leverages Artificial Intelligence (AI) and Virtual Web of Things (IoT) technologies to streamline stock handling, demand forecasting, and manufacturing decisions within the material industry.

**Key Goals:**
1.  **Optimize Stock Levels**: To design an AI-powered solution that accurately tracks and predicts stock availability—raw materials, in-process products, and finished products—thereby minimizing overstocking and understocking circumstances.
2.  **Execute Virtual IoT Monitoring**: To reenact IoT-based temperature, stickiness (humidity), and smoke sensors utilizing platforms like Wokwi, ThingsBoard, and Ubidots with Arduino Uno. These virtual sensors ensure fabric security and alarm stock managers about potential environmental dangers such as fire or dampness (moisture) damage.
3.  **Enable Real-Time Demand Forecasting**: To apply machine learning algorithms for analyzing historical sales information and market patterns, thus enabling the framework to predict fabric demand in progress and support timely restocking decisions.
4.  **Predict Fabric Pricing Accurately**: To utilize AI models that consider various variables (market trends, crude fabric costs, competitor pricing) for determining fabric costs, allowing material producers to stay competitive and profitable.
5.  **Support Sustainable Practices**: To propose eco-friendly squander (waste) reusing methods using trained ML models (like Arbitrary Woodland/Random Forest) for superior squander administration, contributing to sustainability in material manufacturing.
6.  **Assist in Interchange Item Proposals**: To intelligently recommend interchange fabric or product manufacturing alternatives based on availability of resources and current market demand, enhancing versatility and reducing downtime.
7.  **Enhance Fire Security and Risk Management**: To integrate a fire alarm system that virtually detects unusual temperature, smoke, and light changes to prevent mischances and minimize misfortunes in texture capacity areas.

## Scope
The scope of this project extends over stock optimization, AI-driven analytics, virtual IoT integration, and real-time choice support for the material industry. It is built to help producers and stock managers in dealing with critical operations such as demand forecasting, cost expectation, fire security, and economical squander administration through a keen, automated solution.

1.  **Mechanical Application within the Material Segment**: This framework is particularly designed for material producers where various stock types—raw materials, handling units, and finished goods—are managed daily. The scope includes monitoring and managing these stock types to ensure an efficient supply chain and continuous generation flow. The capacity to track stock levels in real time and predict deficiencies enables superior planning and cost-saving.
2.  **Integration of Virtual IoT Innovation**: With limited access to physical sensors, the framework employs virtual IoT platforms like Wokwi and Ubidots to simulate temperature, mugginess (humidity), and smoke detection through Arduino Uno. This enables the monitoring of environmental conditions that could harm fabric materials, ensuring secure capacity and proactive action against dangers such as fire or mold.
3.  **Artificial Intelligence for Forecasting and Choice Support**: By coordinating machine learning models into the backend, the framework supports demand forecasting, cost expectation, and alternative item recommendations. Algorithms such as Straight Relapse (Linear Regression), Arbitrary Woodland (Random Forest), and Choice Trees enable predictive analytics that assist managers in planning acquirement, manufacturing plans, and estimating methodologies.
4.  **Sustainability and Waste Management**: An essential part of the framework is its squander (waste) reusing recommendation module, which employs AI to suggest transfer or reuse methods for remaining textures and squander materials. This encourages sustainability in the manufacturing process and aligns with modern environmental regulations.
5.  **User-Friendly Web Interface**: The framework incorporates a web application built using HTML, CSS, and JavaScript, with backend support from Flask (Python). It allows clients to view stock status, get real-time alarms, access predictions, and manage tasks through an intuitive dashboard. The net interface also enables seamless integration of virtual IoT information and AI comes about for centralized decision-making.
6.  **Adaptability and Future Extension**: While initially designed for materials, the architecture of this framework can be expanded to other manufacturing divisions, counting gadgets, pharmaceuticals, and automotive.

## Expected Outcomes
1.  **Improved Inventory Accuracy and Availability**: One of the major expected outcomes is achieving real-time visibility of inventory levels, including raw materials, manufacturing items, and finished goods. By implementing stock tracking and threshold-based monitoring, the system ensures that stockouts and overstocking situations are minimized, improving production efficiency and reducing idle time in the manufacturing pipeline.
2.  **Accurate Demand Forecasting and Pricing Strategies**: The use of machine learning models is expected to result in highly accurate predictions of product demand based on historical trends and seasonal behaviors. This allows textile industries to adjust production volumes, pricing strategies, and marketing efforts accordingly. Likewise, price prediction models will help manufacturers remain competitive and profitable by dynamically suggesting optimal pricing.
3.  **Virtual IoT-Based Alerts for Environmental Risks**: With the simulation of sensors such as temperature, humidity, and smoke detectors using Arduino Uno and Wokwi, the system will generate virtual alerts when critical conditions are detected. This outcome enables early action to prevent damage to sensitive materials, particularly fabrics prone to humidity and heat exposure, ensuring better quality control and asset protection.
4.  **Sustainable Waste Management Suggestions**: By analyzing waste fabric data through a Random Forest Classifier, the system will provide automated recommendations for fabric reuse, recycling, or safe disposal. This contributes to a greener production process, promoting sustainability and minimizing landfill contributions.
5.  **Efficient Fire Detection and Safety Measures**: The inclusion of a fire detection module using LDRs, MQ2 smoke sensors, and DHT22 readings is expected to enable fast and accurate identification of potential fire hazards. This system helps protect not only physical assets but also personnel working in the facility by generating alarms and on-screen alerts through a buzzer, LED, and LCD setup.
6.  **User Empowerment Through Web Dashboard**: Users will benefit from an easy-to-use web interface to monitor stock, receive AI insights, respond to alerts, and make informed decisions. The dashboard consolidates information from both AI models and virtual sensors to create a centralized decision hub for stock managers and plant operators.

## Features
* **AI-Powered Predictions**: Uses machine learning models (Linear Regression, Random Forest, Decision Trees) for accurate demand forecasting, price prediction, and waste management, significantly reducing guesswork and manual errors.
* **IoT Integration (Virtual)**: Incorporates simulated IoT sensors (Arduino Uno) for temperature, humidity, fire detection, and RFID tracking, offering real-time monitoring without needing physical hardware.
* **Real-Time Alerts**: Sends timely alerts for low stock, high demand, fire risks, and fabric storage issues, ensuring prompt action by managers.
* **Fabric Damage Prevention**: Monitors environmental conditions and recommends relocation of fabrics at risk due to high temperature or humidity, safeguarding sensitive materials.
* **Waste Recycling Suggestions**: Recommends eco-friendly disposal or recycling methods using AI classification techniques (like Random Forest), thereby reducing environmental impact and promoting sustainability.
* **Stock Optimization**: Helps maintain optimal inventory levels by predicting future needs and automating restocking suggestions, minimizing both overstocking and stockouts.
* **Web-Based Interface**: Features a user-friendly web application built using HTML/CSS/JavaScript and a Flask backend, making it accessible for stock managers from anywhere.
* **Data-Driven Decision Making**: Significantly enhances operational efficiency, reduces manual workload, and supports informed, data-driven decision-making.

## Technologies Used

**Hardware (Virtual/Simulated):**
* Arduino Uno (Virtual using Wokwi)
* DHT22 Sensor (Temperature & Humidity)
* MQ-2 Smoke Sensor
* Buzzer, LED, LDR, LCD Display

**Software & Frameworks:**
* **Programming Languages**: Python, C/C++, JavaScript, HTML, CSS
* **Backend Framework**: Flask (Python)
* **Frontend Tools**: VS Code, Arduino IDE
* **Python Libraries**: `pandas`, `scikit-learn` (`sklearn`), `matplotlib`, `Flask`, `unittest`, `PySerial`
* **IoT Platforms (Virtual)**: ThingsBoard, Ubidots

## System Architecture
The system follows a typical web application architecture with a distinct backend and frontend, integrated with virtual IoT components:

* **Frontend**: Developed using HTML, CSS, and JavaScript to provide an interactive web dashboard for user interaction.
* **Backend**: Powered by Flask (Python), handling all the AI logic, data processing, database interactions, and API endpoints for communication with the frontend.
* **Machine Learning Models**:
    * **Linear Regression**: For price prediction.
    * **Decision Tree**: For demand forecasting.
    * **Random Forest**: For recycling suggestions and waste management.
* **Data Storage**: CSV files are used for managing stock, demand, and waste data.
* **Virtual IoT**: Arduino Uno with DHT22 and MQ-2 sensors simulate real-time environmental data, which is then processed via Arduino Uno and displayed on the dashboard.

*(Consider adding a Component Diagram and Data Flow Diagram here if you have them as images. You can link them or embed them, e.g., `![Component Diagram](path/to/your/component_diagram.png)`)*

## Installation Guide

To set up and run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Set up the Python Environment:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Python dependencies:**
    *(You'll need to create a `requirements.txt` file in your project root containing all the Python libraries listed above, e.g., `Flask`, `pandas`, `scikit-learn`, `pyserial`, etc.)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Virtual IoT (if applicable):**
    * Set up your virtual Arduino environment (e.g., Wokwi) and connect it to your chosen IoT platform (ThingsBoard/Ubidots).
    * Ensure the serial communication settings in your Python backend match your virtual Arduino setup.

5.  **Run the Flask application:**
    ```bash
    python app.py  # Or whatever your main Flask app file is named
    ```

6.  **Access the web interface:**
    Open your web browser and navigate to `http://127.0.0.1:5000` (or the address shown in your terminal).

## Usage
* **Dashboard**: View real-time stock levels, demand predictions, and IoT sensor data.
* **Inventory Management**: Update stock details, add new fabric types, and manage existing inventory.
* **Alerts**: Respond to automated alerts for low stock, high demand, and environmental hazards.
* **Suggestions**: Utilize AI-driven recommendations for recycling and waste reduction.

## Complexity Analysis

**Time Complexity:**
Most data filtering and processing tasks within the project have a linear time complexity of **O(n)**, where 'n' is the number of rows in the dataset. This includes operations like filtering stock and demand data based on various conditions. Training machine learning models, such as Linear Regression, also exhibits **O(n)** complexity (where 'n' is the number of samples). For Random Forest training, it's **O(t \* n \* log n)**, where 't' is the number of trees. Serial data reading is **O(1)** per line read.

**Space Complexity:**
The largest storage requirement comes from the Pandas DataFrames (`stock_df`, `demand_df`, `fabric_data`), which require space proportional to their size (**O(n)** rows and **O(k)** columns). Machine learning models also consume space, typically **O(t \* d)** for Random Forest (where 't' is the number of trees and 'd' is the number of features). Serial data storage is also **O(n)** based on the number of data points collected.

Overall, the project is designed for scalability with linear growth rates in both time and space complexities for most operations, making it suitable for moderately sized datasets.

## Team Members
* Ms. A. Akshaya (21ME1A05D3)
* Mr. Ch. Jaswanth (21ME1A05E2)
* Ms. G. Vyshnavi (21ME1A05E9)
* Ms. D. Naga Pavan (21ME1A05E6)

**Mentor**: Mrs. D. Tejaswi, Assistant Professor, Department of Computer Science and Engineering.

## Acknowledgements
We extend our sincere gratitude to Mrs. D. Tejaswi for her invaluable guidance and support throughout this project. We also acknowledge the resources and tools that made this project possible.

