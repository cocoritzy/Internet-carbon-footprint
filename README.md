### What is Internet carbon emission?
As internet usage continues to grow, it contributes significantly to global electricity consumption and greenhouse gas (GHG) emissions. Internet data traffic currently accounts for **7% of global electricity consumption** and **3.5% of global GHG emissions**. If left unchecked, this could rise to **14% of GHG emissions by 2040**. This project explores whether real-time monitoring and personalized feedback on internet usage can influence users to reduce their digital carbon footprint.

---

### My Concept
A **data-driven approach to internet carbon awareness**:
1. **Collect**: Track real-time internet usage data using network traffic analysis.
2. **Analyze**: Use machine learning to classify internet activities and calculate their carbon footprint.
3. **Actuate**: Provide personalized feedback and tips to users to reduce their carbon emissions.
4. **Visualize**: Display real-time carbon footprint data via a web app.
<img src="https://github.com/user-attachments/assets/fbd66a57-d8c2-423e-be01-b8d9c1eb24d5" width="50%" />

### Architecture

- **Hardware**: 
  - User computers equipped with network traffic monitoring tools and RasberryPi.
- **APIs**:
  - **Google Cloud Storage API**: Stores collected network traffic data.
  - **IP Location API**: Retrieves the location of data centers to calculate carbon intensity.
- **Cloud**:
  - **Google Cloud Platform**: Hosts data storage and processing.
- **Data Analysis**:
  - **Machine Learning (Random Forest Classifier)**: Classifies network traffic into 35 applications.
  - **Carbon Footprint Calculation**: Converts data traffic (GB) to carbon emissions (CO₂e) using location-based carbon intensity.
- **Web App**:
  - **Python Dash Framework**: Visualizes real-time carbon footprint data and provides personalized feedback.
<img src="https://github.com/user-attachments/assets/f3e08c8c-3280-4fc6-825f-d80843a28acb" width="50%" />

---

### Data Collection & Analysis
- **Internet Usage Data**: Collected using **Wireshark** and **Pyshark**, stored in Google Cloud Storage.
- **Carbon Footprint Calculation**:
  - Data traffic is classified by application using a Random Forest model.
  - Carbon emissions are calculated by converting data traffic (GB) to energy (kWh) and then to CO₂e using location-specific carbon intensity.
- **Analysis**:
  - **User Behavior**: Breakdown of internet activities (e.g., video streaming, email, social media) and their carbon impact.
  - **Behavioral Impact**: Personalized feedback and tips are provided to users to encourage energy-saving behavior.

---

### The Results (So Far!)
- **Correlation**: The tool successfully classified **35 internet applications** and calculated their carbon footprint with high accuracy (**98% precision**).
- **Behavioral Impact**: Users in the experimental group, who received personalized feedback, reduced their carbon emissions by **27%** compared to the control group.
- **Web App**: Real-time carbon footprint data was visualized via a web app, providing users with insights into their internet usage and carbon emissions

---

This project was powered by **Google Cloud Platform**, **Wireshark**, and **Python Dash**, demonstrating how real-time monitoring and personalized feedback can effectively reduce internet-related carbon emissions.
