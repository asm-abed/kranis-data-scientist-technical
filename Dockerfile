# Use the official Python 3.9 image
FROM python:3.9.1

# Install cron and any other dependencies (PostgreSQL client, etc.)
RUN apt-get update && apt-get install -y cron

# Set the working directory in the container
WORKDIR /app

# Copy the requirements to the container
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your Python scripts into the container
COPY fetch_weather_data.py upload_daily_weather_data.py analyze_data.py /app/

# Copy the cron job configuration
COPY cronjob /etc/cron.d/cronjob

# Give execution rights on the cron job file
RUN chmod 0644 /etc/cron.d/cronjob

# Apply cron job
RUN crontab /etc/cron.d/cronjob

# Expose port for database
EXPOSE 5432
