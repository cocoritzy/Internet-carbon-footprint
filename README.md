### What is Internet carbon emission?

The I.C.E tool is a real-time Internet carbon footprint analyser to encourage behaviour change through increasing user awareness
---
### 🔍 The Problem
Streaming videos, sending emails, and editing documents are all examples of activities that are responsible for an individual’s ever-increasing data consumption. Several solutions focusing on the IT hardware have been developed in recent years, but the increase of the Internet users’ data consumption lacks attention, becoming a threat to a viable digital future. 
Internet traffic is predicted to grow at a compound annual growth rate (CAGR) of 26 % in the coming years . Due to this dramatic growth, Internet data traffic represents already 7% of the global electricity consumption, producing 3.5%, of global greenhouse gas (GHG) emissions. In this context, if nothing is done, the carbon footprint of total internet traffic could reach 14% of GHG by 2040.
Two major problems persist:

- **Lack of awareness:** The carbon footprint of the internet is invisible, making users unaware of its environmental impact.
- **Inaccurate measurement:** Current tools for measuring internet carbon footprints are often unreliable, with estimates varying by up to five orders of magnitude.

### My Concept
A **data-driven approach to internet carbon awareness**:
1. **Collect**: Track real-time internet usage data using network traffic analysis.
2. **Analyze**: Use machine learning to classify internet activities and calculate their carbon footprint.
3. **Actuate**: Provide personalized feedback and tips to users to reduce their carbon emissions.
4. **Visualize**: Display real-time carbon footprint data via a web app.
<img src="https://github.com/user-attachments/assets/fbd66a57-d8c2-423e-be01-b8d9c1eb24d5" width="50%" />

### Architecture

- **Hardware**: 
  - User computers equipped with network traffic monitoring (wireshark) tools and RasberryPi.
- **APIs**:
  - **Google Cloud Storage API**: Stores collected network traffic data.
  - **IP Location API**: Retrieves the location of data centers to calculate carbon intensity.
- **Cloud**:
  - **Google Cloud Platform**: Hosts data storage and processing.
- **Data Analysis**:
  - **Machine Learning (Random Forest Classifier)**: Classifies network traffic into 35 applications.
  - **Carbon Footprint Calculation**: Converts data traffic (GB) to carbon emissions (CO₂e) using location-based carbon intensity
- **Web App**:
  - **Python Dash Framework**: Visualizes real-time carbon footprint data and provides personalized feedback.
<img src="https://github.com/user-attachments/assets/f3e08c8c-3280-4fc6-825f-d80843a28acb" width="50%" />

---

### Data Collection & Analysis
- **Internet Usage Data**: Collected using **Wireshark** and **Pyshark**, stored in Google Cloud Storage.
- **Carbon Footprint Calculation**:
  - Data traffic is classified by application using a Random Forest model.
  - Carbon emissions are calculated by converting data traffic (GB) to energy (kWh) and then to CO₂e using location-specific carbon intensity.
 
  ```

    Total Carbon Footprint (gCO2) = 
        (W_Data_Centers × C_i_ip + W_End_users × C_i_uk) 
        + (W_Transmission_equipment + W_Manufacturing_and_production) 
        × C_i_world × E_internet

    Where:

    - W represents the weight per segment:
        - W_Data Centers = 0.15
        - W_End users = 0.52
        - W_Transmission_equipment = 0.14
        - W_Manufacturing_and_production = 0.15
    - C_i_world = World carbon intensity (gCO₂/kWh)
    - C_i_ip = Data Centers carbon intensity (gCO₂/kWh) 
    - C_i_uk = UK grid carbon intensity (gCO₂/kWh)
    - E_internet = Internet energy consumption (kWh)
- **Analysis**:
  - **User Behavior**: Breakdown of internet activities (e.g., video streaming, email, social media) and their carbon impact.
  - **Behavioral Impact**: Personalized feedback and tips are provided to users to encourage energy-saving behavior.

---

### The Results (So Far!)
- **Correlation**: The tool successfully classified **35 internet applications** and calculated their carbon footprint with high accuracy (**98% precision**).
- **Behavioral Impact**: Users in the experimental group, who received personalized feedback, reduced their carbon emissions by **27%** compared to the control group.
- **Web App**: Real-time carbon footprint data was visualized via a web app, providing users with insights into their internet usage and carbon emissions

### References
    - Aslan et al. (2018) - Electricity intensity of Internet data transmission.
    - Andrae & Edler (2015) - Global electricity usage of communication technology.
    - Greenpeace’s Click Clean Report (2016) - Breakdown of data traffic per application.     
---

This project was powered by **Google Cloud Platform**, **Wireshark**, and **Python Dash**, demonstrating how real-time monitoring and personalized feedback can effectively reduce internet-related carbon emissions.
