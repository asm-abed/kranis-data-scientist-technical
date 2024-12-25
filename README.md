# kranis-data-scientist-technical

Resources Used:
- Open-Meteo.com as data source
- PostgreSQL
- Cron
- Docker and Docker Compose for containerization
- pgAdmin
- PowerBI

For this system, I chose to use Docker to containerize everything for convenience and efficiency. Docker Compose allows setup of the whole system with a single command. This also allows easy scheduling of jobs that are needed to run at specific times. 


How to run this:

1. Download the repository or run codespaces here in GitHub, and if possible, connect it to VSCode Desktop on your machine. 
2. Run **`docker-compose up`** and wait for everything to load up.
3. Once all is up and running, go to PORTS and click the link to the 8080 port. That will go to the pgAdmin login page. Use the following credentials to log in:
    - Email: admin@admin.com
    - Password: root
    - PS: If it doesn't load, you can try to connect Codespace to VSCode Desktop instead.
4. You should see "Servers" on the left-hand side. Right-click that, then click *Register..* > Server.
5. Server Name can be anything but is required.
6. Go to the Connections tab and input the following:
    - Host name/address: pgdatabase
    - User: root
    - Password: root
    Then click Save.
7. That should get you in. Navigate to Databases > weather_data > Schemas > Tables > weather_data, right-click, then View/Edit Data.
8. To run the Data Analysis Script: **`python analyze_data.py`**. This will log averages as requested and download a plot of temperatures.
9. The Cron has also been automatically set up. You can check the file: `upload_daily_weather_data.py` to see the script being used for the Cronjob and the file `cronjob` for the specific schedule.
10. For Power BI, you can get the data from PostgreSQL by following these steps:
      a. Download the psqlodbc driver: [Download Link](https://ftp.postgresql.org/pub/odbc/releases/REL-17_00_0004-mimalloc/psqlodbc-setup.exe)
      b. Install the file on your machine. Open PowerBI Desktop, then click *Get Data* > Connect.
      c. Select ODBC.
      d. Set Data Source to None and click the advanced option.
      e. Copy this: `Driver={PostgreSQL ANSI(x64)}; Server=localhost; Port=5432; Database=weather_data`, then connect.
