"""
    Weather Module
        
    Functions
    
        get_lat_lon(city)
            return lattitude and longitude of given city or False if city not available
        get_temprature(lat, lon)
            return temprature dict or empty dictionary if city data not available
            temprature dict = {
               
                "name": name,
                "temp": temp,
                "desc": desc,
                "icon": f"https://openweathermap.org/img/wn/{icon}@4x.png" 
            }
            
"""

import requests
import os

def get_lat_lon(city):
    """
    return lattitude and longitude of given city or False if city not available
    """
    city = city.strip().lower()
    url = "https://api.openweathermap.org/data/2.5/weather"
    parameters = {
        "q": city,
        "appid": "4db018eff1800d85dc793494f36ed372"
    }
    resp = requests.get(url, params=parameters)
    if resp.status_code == 200:
        try:
            data = resp.json()
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]
            return lat, lon
        except:
            return False
    return False
        

def get_temprature(lat, lon):
    """return temprature dict or empty dictionary if city data not available
            temprature dict = {
                "data": data,
                "name": name,
                "temp": temp,
                "desc": desc,
                "icon": f"https://openweathermap.org/img/wn/{icon}@4x.png" 
            }
    """
    url = "https://api.openweathermap.org/data/2.5/weather"

    parameters = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid":   "4db018eff1800d85dc793494f36ed372"
    }
    resp = requests.get(url, params=parameters)
    if resp.status_code == 200:
        try:
            data = resp.json()
            name = data["name"]
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            icon = data["weather"][0]["icon"]
            return {
                "name": name,
                "temp": temp,
                "desc": desc,
                "icon": f"https://openweathermap.org/img/wn/{icon}@4x.png" 
            }
        except Exception as e:
            print("Error!", e)
            return {}
    else:
        print("\nSomething Went Wrong")
        print(f"Status Code: {resp.status_code} {resp.reason}")
        return {}
    
if __name__ == "__main__":
    os.system("cls")
    print("\n\n\n")
    city = input("Enter City Name: ".rjust(50))
    coord = get_lat_lon(city)
    if coord:
        lat, lon = coord
        data = get_temprature(lat, lon)
        for key, value in data.items():
            print(f"{key:>30} = {value}")
        print("\n\n\nn")
    else:
        print("City Not Found!")
