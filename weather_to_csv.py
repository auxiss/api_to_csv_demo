import requests
import csv

import sys
from typing import List, Dict

def params() -> Dict:
    args = sys.argv[1:]

    result = {
        "filename": None,
        "lat": None,
        "lon": None,
        "verbose": False
    }

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "-f" and i + 1 < len(args):
            result["filename"] = args[i + 1]
            i += 1

        elif arg == "-lat" and i + 1 < len(args):
            result["lat"] = float(args[i + 1])
            i += 1

        elif arg == "-lon" and i + 1 < len(args):
            result["lon"] = float(args[i + 1])
            i += 1

        elif arg == "-v":
            result["verbose"] = True

        i += 1


    if result["filename"] is None:
        print("Error: filename is required. Use -f <filename> to specify it.")
        sys.exit(1)
    if result["lat"] is None:
        print("Error: latitude is required. Use -lat <latitude> to specify it.")
        sys.exit(1)
    if result["lon"] is None:
        print("Error: longitude is required. Use -lon <longitude> to specify it.")
        sys.exit(1)

    return result





def json_to_csv(json_data, filename, verbose=False) -> None:
    
    fields = []

    #convert json to dict
    dict_data = {}

    for key, value in json_data.items():
        if verbose: print(f"Processing key: {key}")
        

        if key == "current_weather" or key == "current_weather_units":
            pass
        else:
            if verbose: print(f"{key}: {value}")
            fields.append(key)
            dict_data[key] = value


    for key, value in json_data["current_weather"].items():
        if verbose: print(f"Processing key: {key}")

        val = f'{str(value)} {json_data["current_weather_units"].get(key, "")}'   #hire i keep the value and the unit together in one field.
        if verbose: print(f"{key}: {val}")

        fields.append(key)
        dict_data[key] = val

    

    #write dict to csv
    try:    #check if file exists

        with open(f"{filename}.csv", "r") as file:
            print(f"File {filename}.csv already exists. adding data to it.")
            reader = csv.DictReader(file)
            existing_data = list(reader)
            existing_data.append(dict_data)

        with open(f"{filename}.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(existing_data)


    except FileNotFoundError:
        print(f"File {filename}.csv does not exist. It will be created.")

        with open(f"{filename}.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)

            writer.writeheader()
            writer.writerows([dict_data])
    







if __name__ == "__main__":
    

    p = params()
    print(p)

    file_name = p["filename"]
    latitude = p["lat"]
    longitude = p["lon"]

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    response = requests.get(url, params=params)

    data = response.json()

    json_to_csv(data, file_name)




