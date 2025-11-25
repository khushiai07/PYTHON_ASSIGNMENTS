import pandas as pd 
from pathlib import Path
from dashboard import generate_dashboard
import os


os.makedirs('output', exist_ok=True)


def ingest_data(data_folder='data'):
    
    data_path = Path(data_folder)
    all_files = list(data_path.glob('*.csv'))
    
    if not all_files:
        print(f"No CSV files found in {data_folder}")
        return pd.DataFrame()

    df_list = []
    
    print(f"Found {len(all_files)} files. Starting ingestion...")

    for file in all_files:
        try:
            building_name = file.stem
            
            df_temp = pd.read_csv(file, on_bad_lines='skip')
            

            required_cols = {'timestamp', 'kwh'}
            if not required_cols.issubset(df_temp.columns):
                print(f"[WARNING] Skipping {file.name}: Missing columns {required_cols - set(df_temp.columns)}")
                continue
                
            df_temp['timestamp'] = pd.to_datetime(df_temp['timestamp'], errors='coerce')
            
            if df_temp['timestamp'].isna().any():
                invalid_count = df_temp['timestamp'].isna().sum()
                print(f"[INFO] Dropped {invalid_count} rows with invalid dates in {file.name}")
                df_temp = df_temp.dropna(subset=['timestamp'])

            df_temp['Building_Name'] = building_name
            
            df_list.append(df_temp)
            print(f"[SUCCESS] Loaded {file.name} ({len(df_temp)} rows)")
            
        except Exception as e:
            print(f"[ERROR] Failed to process {file.name}: {e}")

    if df_list:
        df_combined = pd.concat(df_list, ignore_index=True)
        return df_combined
    else:
        return pd.DataFrame()

# --- Execution Block ---
if __name__ == "__main__":
    df_master = ingest_data()
    
    print("\n--- Master DataFrame Info ---")
    print(df_master.info())
    print("\n--- First 5 Rows ---")
    print(df_master.head())
    

def generate_summary_report(building_manager, df_master, output_folder='output'):
    os.makedirs(output_folder, exist_ok=True)
    
    clean_data_path = os.path.join(output_folder, 'cleaned_energy_data.csv')
    df_master.to_csv(clean_data_path)
    print(f"[REPORT] Saved cleaned data to {clean_data_path}")

    summary_list = []
    for building in building_manager.list_buildings():
        stats = building.get_summary_stats()
        if stats:
            summary_list.append(stats)
    
    df_summary = pd.DataFrame(summary_list)
    summary_csv_path = os.path.join(output_folder, 'building_summary.csv')
    df_summary.to_csv(summary_csv_path, index=False)
    print(f"[REPORT] Saved summary stats to {summary_csv_path}")

    total_campus_kwh = df_summary['Total (kwh)'].sum()
    highest_building = df_summary.loc[df_summary['Total (kwh)'].idxmax()]
    
    global_hourly = df_master.groupby('timestamp')['kwh'].sum()
    peak_time = global_hourly.idxmax()
    peak_load = global_hourly.max()

    report_content = f"""
CAMPUS ENERGY ANALYSIS REPORT
=============================
Date Generated: {pd.Timestamp.now()}

1. GLOBAL STATISTICS
--------------------
Total Campus Consumption: {total_campus_kwh:,.2f} kwh
Peak Campus Load: {peak_load} kwh occurred at {peak_time}

2. BUILDING HIGHLIGHTS
----------------------
Highest Consuming Building: {highest_building['Building']}
   - Total Usage: {highest_building['Total (kwh)']:,.2f} kwh
   - Average Hourly Usage: {highest_building['Mean (kwh)']:.2f} kwh

3. DATA SUMMARY
---------------
Total Buildings Analyzed: {len(df_summary)}
Data Records Processed: {len(df_master)}
    """
    
    txt_path = os.path.join(output_folder, 'summary.txt')
    with open(txt_path, 'w') as f:
        f.write(report_content)
        
    print(f"[REPORT] Executive summary written to {txt_path}")


class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = float(kwh)
        
    def __repr__(self):
        return f"reading({self.timestamp}, {self.kwh} kwh)"
    
class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []
    
    def add_reading(self, timestamp, kwh):
        reading = MeterReading(timestamp, kwh)
        self.meter_readings.append(reading)
    
    def get_dataframe(self):
        
        data = {
            'timestamp': [r.timestamp for r in self.meter_readings],
            'kwh': [r.kwh for r in self.meter_readings]
        }
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    
    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)
    
    def calculate_daily_totals(self):
        df = self.get_dataframe()
        
        if df.empty:
            return pd.Series()
        
        return df.resample('D')['kwh'].sum()
    
    def calculate_weekly_average(self):
        df = self.get_dataframe()
        
        if df.empty:
            return pd.Series()
        
        return df.resample('W')['kwh'].mean()
    
    def get_summary_stats(self):
        
        df = self.get_dataframe()
        
        if df.empty:
            return {}
        
        return {
            "Building": self.name,
            "Total (kwh)": df['kwh'].sum(),
            "Mean (kwh)": df['kwh'].mean(),
            "Max (kwh)": df['kwh'].max(),
            "Min (kwh)": df['kwh'].min()
        }
        
class BuildingManager:
    def __init__(self):
        self.buildings = {} 

    def get_or_create_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        
        return self.buildings[name]
    
    def list_buildings(self):
        return list(self.buildings.values())
        
        

manager = BuildingManager()

print("Populating Object Model...")
        
for index, row in df_master.iterrows():
    
    building = manager.get_or_create_building(row['Building_Name'])
    
    building.add_reading(row['timestamp'], row['kwh'])
    

generate_dashboard(manager)
generate_summary_report(manager, df_master)