from sqlalchemy import create_engine, text
import pandas as pd
import fetch_weather_data
import psycopg2

# Connect to Postgres
engine = create_engine('postgresql://root:root@localhost:5432/weather_data')

weather_week = fetch_weather_data.get_weather_7days(longitude=121.0614, latitude=14.5869, city = "Pasig City, Philippines", timezone="Asia/Singapore")

print(len(weather_week))
# Uploading the data to the setup postgresql database

# Upload the data to the database
weather_week.head(n=0).to_sql(name="weather_data", con=engine, if_exists='replace')  # Create table without data
weather_week.to_sql(name="weather_data", con=engine, if_exists='append')  # Append data

# Add a surrogate key and set it as the primary key
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE weather_data ADD COLUMN id SERIAL PRIMARY KEY;"))

