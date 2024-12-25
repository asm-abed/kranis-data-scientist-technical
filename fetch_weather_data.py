import openmeteo_requests
import requests_cache
from sqlalchemy import create_engine, text
import pandas as pd
from retry_requests import retry

weather_codes = {
    0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast', 45: 'Fog', 48: 'Depositing rime fog',
    51: 'Drizzle: Light intensity', 53: 'Drizzle: Moderate intensity', 55: 'Drizzle: Dense intensity',
    56: 'Freezing Drizzle: Light intensity', 57: 'Freezing Drizzle: Dense intensity', 61: 'Rain: Slight intensity',
    63: 'Rain: Moderate intensity', 65: 'Rain: Heavy intensity', 66: 'Freezing Rain: Light intensity', 67: 'Freezing Rain: Heavy intensity',
    71: 'Snow fall: Slight intensity', 73: 'Snow fall: Moderate intensity', 75: 'Snow fall: Heavy intensity', 77: 'Snow grains',
    80: 'Rain showers: Slight intensity', 81: 'Rain showers: Moderate intensity', 82: 'Rain showers: Violent intensity',
    85: 'Snow showers: Slight intensity', 86: 'Snow showers: Heavy intensity', 95: 'Thunderstorm: Slight or moderate',
    96: 'Thunderstorm with slight hail', 99: 'Thunderstorm with heavy hail'
}


def daily_weather_data(latitude, longitude, city, timezone='Asia/Singapore', weather_codes=weather_codes):
     
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # API parameters
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': ['temperature_2m', 'relative_humidity_2m', 'weather_code'],
        'timezone': timezone,
        'forecast_days': 1
    }

    # Fetch weather data
    weather_data = openmeteo.weather_api(url, params=params)

    # Process first location
    response = weather_data[0]

   # Current values (assuming the same order as requested in the API call)
    data = response.Hourly()
    

    weather_fc = {"timestamp": pd.date_range(
        start = pd.to_datetime(data.Time(), unit = "s", utc = True),
        end = pd.to_datetime(data.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = data.Interval()),
        inclusive = "left"
    )}
    
    variable_names = ['temperature', 'humidity', 'weather_code']
    for i, name in enumerate(variable_names):
        weather_fc[name] = data.Variables(i).ValuesAsNumpy()


    weather_fc['city'] = city

    weather_df = pd.DataFrame(data = weather_fc)

    weather_df['weather_description'] = weather_df['weather_code'].apply(
        lambda code: weather_codes.get(code, 'Unknown')
    )

    weather_df = weather_df[['timestamp', 'city', 'temperature', 'humidity', 'weather_description']]
    return weather_df

def get_weather_7days(latitude, longitude, city, timezone='Asia/Singapore', weather_codes = weather_codes):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': ['temperature_2m', 'relative_humidity_2m', 'weather_code'],
        'timezone': timezone,
        'past_days': 7,
	    "forecast_days": 1
    }

    # Fetch weather data
    weather_data = openmeteo.weather_api(url, params=params)

    # Process first location
    response = weather_data[0]

    # Current values (assuming the same order as requested in the API call)
    data = response.Hourly()
    

    weather_fc = {"timestamp": pd.date_range(
        start = pd.to_datetime(data.Time(), unit = "s", utc = True),
        end = pd.to_datetime(data.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = data.Interval()),
        inclusive = "left"
    )}
    
    variable_names = ['temperature', 'humidity', 'weather_code']
    for i, name in enumerate(variable_names):
        weather_fc[name] = data.Variables(i).ValuesAsNumpy()


    weather_fc['city'] = city

    weather_df = pd.DataFrame(data = weather_fc)

    weather_df['weather_description'] = weather_df['weather_code'].apply(
        lambda code: weather_codes.get(code, 'Unknown')
    )

    weather_df = weather_df[['timestamp', 'city', 'temperature', 'humidity', 'weather_description']]
    return weather_df


### To get started on the database, the following script will upload weather data from the last 7 days


# Connect to Postgres
engine = create_engine('postgresql://root:root@pgdatabase:5432/weather_data')

weather_week = get_weather_7days(longitude=121.0614, latitude=14.5869, city = "Pasig City, Philippines", timezone="Asia/Singapore")

# Uploading the data to the setup postgresql database

# Upload the data to the database
weather_week.head(n=0).to_sql(name="weather_data", con=engine, if_exists='replace')  # Create table without data
weather_week.to_sql(name="weather_data", con=engine, if_exists='append')  # Append data

# Add a surrogate key and set it as the primary key
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE weather_data ADD COLUMN id SERIAL PRIMARY KEY;"))

