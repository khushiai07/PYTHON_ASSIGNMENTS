import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# 1. Create the data directory
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# 2. Define settings
buildings = ['A_block', 'B_block', 'C_block']
start_date = "2025-11-01"
end_date = "2025-11-30 23:00:00"

# Generate a date range
timestamps = pd.date_range(start=start_date, end=end_date, freq='H')

# 3. Generate data for each building
for building in buildings:
    if building == 'A_block':
        base_load = 50 
        variance = 20
    elif building == 'B_block':
        base_load = 40
        variance = 10
    else:
        base_load = 35  
        variance = 5

    # Generate random kWh readings with some realistic patterns
    readings = []
    for ts in timestamps:
        # Add a peak hour (higher usage between 9 AM and 6 PM)
        if 9 <= ts.hour <= 18:
            hourly_kwh = base_load + np.random.randint(10, 30)
        else:
            hourly_kwh = base_load + np.random.randint(0, 10)
            
        if np.random.random() < 0.005:
             hourly_kwh = 0 
             
        readings.append(hourly_kwh)

    df = pd.DataFrame({
        'timestamp': timestamps,
        'kwh': readings
    })

    # 4. Save to CSV
    file_path = os.path.join(output_dir, f"{building}.csv")
    df.to_csv(file_path, index=False)
    print(f"Generated {file_path} with {len(df)} rows.")

print("\nData generation complete! Check the '/data' folder.")