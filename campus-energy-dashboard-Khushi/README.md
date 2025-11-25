# Campus Energy Consumption Dashboard

**Author:** Khushi  
**Course:** Programming for Problem Solving using Python  
**Assignment:** Capstone Project - End-to-End Energy Consumption Analysis

## 📌 Project Overview
The campus facilities team is strictly exploring energy-saving opportunities. This Capstone project implements an automated data pipeline to ingest, analyze, and visualize electricity usage data across multiple campus buildings. The goal is to provide actionable insights into daily trends, peak load times, and building-wise efficiency comparisons[cite: 10, 11].

## 📂 Dataset Source
The dataset consists of simulated hourly electricity meter readings (in kWh) generated for three distinct buildings:
* **A_Block** (Simulated Academic Block)
* **B_Block** (Simulated Library)
* **C_Block** (Simulated Hostel)

*Note: The data was programmatically generated using Python to simulate realistic load patterns, including peak hours (9 AM - 6 PM) and random variance.*

## 🛠️ Methodology
This project utilizes a **Data Science Pipeline** approach combined with **Object-Oriented Programming (OOP)** principles[cite: 43].

1.  **Data Ingestion:** * Implemented using `pathlib` to automatically detect and read multiple CSV files from the `/data` directory.
    * Includes robust exception handling for missing files or corrupt data[cite: 22].
2.  **Data Cleaning:** * Validates timestamps and ensures numeric integrity of kWh readings.
    * Merges disparate files into a single Master DataFrame.
3.  **OOP Design:** * **`MeterReading` Class:** Encapsulates individual timestamp/value pairs.
    * **`Building` Class:** Manages aggregation logic (daily totals, weekly averages) using Pandas resampling.
    * **`BuildingManager` Class:** Orchestrates the entire campus model.
4.  **Visualization:** * Generated a unified dashboard using `matplotlib` containing:
        * **Trend Line:** Daily consumption over time.
        * **Bar Chart:** Average weekly usage comparison.
        * **Scatter Plot:** Peak-hour consumption distribution[cite: 66].

## 📊 Key Insights
Based on the analysis of the generated data:
1.  **Peak Load Times:** The scatter plot reveals that the highest energy density occurs consistently between **09:00 and 18:00**, correlating with standard campus operating hours[cite: 83].
2.  **Consumption Variance:** There is a distinct difference in base-load consumption between the academic blocks and the hostel/library, visible in the "Average Weekly Consumption" chart.
3.  **Outliers:** The system successfully handles and flags missing or zero-value readings during the ingestion phase.

## 🚀 How to Run
1.  **Prerequisites:** Ensure Python is installed along with the required libraries:
    ```bash
    pip install pandas matplotlib
    ```
2.  **Execution:** Run the main script from the project root:
    ```bash
    python main.py
    ```
3.  **Output:** Check the `/output` directory for:
    * `dashboard.png` (Visual Analysis)
    * `summary.txt` (Executive Report)
    * `cleaned_energy_data.csv` (Processed Data)

## 📁 Project Structure
```text
campus-energy-dashboard-HarshDabas/
├── data/                   # Raw CSV files
├── output/                 # Generated reports and images
├── main.py                 # Source code (Ingestion, OOP, Viz)
└── README.md               # Project documentation