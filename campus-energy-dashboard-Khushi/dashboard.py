import matplotlib.pyplot as plt
import pandas as pd

def generate_dashboard(building_manager, output_file='output/dashboard.png'):
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 18))
    plt.subplots_adjust(hspace=0.4)
    
    fig.suptitle('Campus Energy Consumption Dashboard', fontsize=20, fontweight='bold')

    # --- Chart 1: Trend Line (Daily Consumption over Time) ---
    ax1.set_title('Daily Energy Consumption Trends', fontsize=14)
    ax1.set_ylabel('Total kWh')
    ax1.set_xlabel('Date')
    
    buildings = building_manager.list_buildings()
    
    for building in buildings:
        daily_data = building.calculate_daily_totals()
        if not daily_data.empty:
            ax1.plot(daily_data.index, daily_data.values, marker='o', linestyle='-', label=building.name)
    
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # --- Chart 2: Bar Chart (Average Weekly Usage) ---
    ax2.set_title('Average Weekly Consumption Comparison', fontsize=14)
    ax2.set_ylabel('Average Weekly kWh')
    
    building_names = []
    weekly_means = []
    
    for building in buildings:
        # Calculate weekly average
        weekly_avg_series = building.calculate_weekly_average()
        if not weekly_avg_series.empty:
            avg_val = weekly_avg_series.mean()
            building_names.append(building.name)
            weekly_means.append(avg_val)
            
    # Create bar chart
    bars = ax2.bar(building_names, weekly_means, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom')

    # --- Chart 3: Scatter Plot (Peak-Hour Consumption) ---
    ax3.set_title('Peak-Hour Consumption Distribution (9 AM - 6 PM)', fontsize=14)
    ax3.set_ylabel('kWh Consumption')
    ax3.set_xlabel('Date & Time')
    
    for building in buildings:
        df = building.get_dataframe()
        if not df.empty:
            peak_data = df.between_time('09:00', '18:00')
            
            ax3.scatter(peak_data.index, peak_data['kwh'], alpha=0.6, label=building.name, s=20)

    ax3.legend(loc='upper right')
    ax3.grid(True, alpha=0.3)

    # --- Save to File --- 
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"[SUCCESS] Dashboard saved to {output_file}")
    