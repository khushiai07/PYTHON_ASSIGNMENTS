# Weather Data Analysis Report

## 1. Introduction
This report analyzes local weather data for the year 2024. The goal was to clean raw data, perform statistical analysis, and visualize trends in Temperature, Rainfall, and Humidity to aid in campus sustainability initiatives.

## 2. Data Processing
* **Source:** Local weather CSV file.
* **Cleaning:** * Dates were converted to standard Datetime objects.
    * Missing values (NaNs) in Temperature and Humidity were filled using the 'Forward Fill' method to maintain continuity.
    * Irrelevant columns were dropped.

## 3. Key Insights

### Temperature Trends
* The **Mean Temperature** for the year was approximately 25°C.
* We observed significant seasonal fluctuation, with peaks occurring mid-year.

### Rainfall Analysis
* Rainfall was aggregated by month.
* The wettest months corresponded with the expected monsoon season, showing high total precipitation in the middle of the year.

### Correlation
* The scatter plot suggests a loose inverse relationship between Temperature and Humidity (as temperature rises, relative humidity often drops, though this varies by season).

## 4. Conclusion
The analysis provides a clean dataset and visual baseline for understanding local climate patterns. These charts can be used to predict optimal times for campus outdoor activities or irrigation planning.