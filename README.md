# api_to_csv_demo
This python script fetches for open-meteo.com and saves them to .csv file.
If file exists the script will append the data else file will be created.

arguments/flags:

-f      filename (no need to add .csv on the end)\n
-lat    latitude of your GPS Coordinates
-lon    longitude of your GPS Coordinates



Example usage:
python weather_to_csv.py -f weather_csv_data -lat 37.967591 -lon 23.71708

