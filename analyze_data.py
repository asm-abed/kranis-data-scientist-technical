import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# PostgreSQL connection details (update as per your Docker Compose setup)
DATABASE_URL = "postgresql://root:root@localhost:5432/weather_data"  # Database connection string

# Create a SQLAlchemy engine for connecting to the PostgreSQL database
engine = create_engine(DATABASE_URL)
engine.connect()

def access_database():
    """
    Fetch weather data for the past 7 days from the PostgreSQL database.
    """
    query = """
    SELECT timestamp, temperature, humidity 
    FROM weather_data
    WHERE timestamp >= NOW() - INTERVAL '3 days'
    ORDER BY timestamp;
    """
    try:
        # Fetch the data into a pandas DataFrame
        df = pd.read_sql(query, engine)
        if df.empty:
            logger.warning("No data found for the past 7 days.")
        return df
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def analyze_data(df):
    """
    Analyze the fetched weather data:
    1. Compute average temperature and humidity
    2. Generate a plot of temperature over time
    """
    if df.empty:
        logger.warning("No data available to analyze.")
        return
    
    # Convert timestamp to datetime (if necessary)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Compute the average temperature and humidity for the past 7 days
    avg_temp = df['temperature'].mean()
    avg_humidity = df['humidity'].mean()
    
    # Log the results
    logger.info(f"Average Temperature for the past 7 days: {avg_temp:.2f} °C")
    logger.info(f"Average Humidity for the past 7 days: {avg_humidity:.2f} %")

    # Generate the temperature plot over time
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['temperature'], label='Temperature (°C)', color='tab:red')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Over the Past 7 Days')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a .png file
    plot_filename = 'temperature_over_time.png'
    plt.savefig(plot_filename)
    plt.close()

    logger.info(f"Plot saved as {plot_filename}")

def main():
    """
    Main function to fetch, analyze, and log the weather data.
    """
    # Fetch the weather data
    df = access_database()
    
    # Analyze the fetched data
    analyze_data(df)

if __name__ == "__main__":
    main()
