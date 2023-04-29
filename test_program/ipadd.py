import requests
import folium
import webbrowser
import os

def get_location(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return f"{data['city']}, {data['regionName']}, {data['country']}"
    return "Unknown"


def get_coordinates(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            print(data['as'])
            return (data['lat'], data['lon'])
    return None

def display_map(coord):
    # create map centered at the given coordinates
    map_center = coord
    map_zoom = 24
    map = folium.Map(location=map_center, zoom_start=map_zoom)

    # add a marker at the center of the map
    marker = folium.Marker(location=map_center)
    marker.add_to(map)

    # save map as an HTML file
    map_file = "map.html"
    map.save(map_file)

    filename = 'file:///'+os.getcwd()+'/' + 'map.html'

    # open map in Chrome
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s" # modify this path to match your Chrome installation location
    webbrowser.get(chrome_path).open(filename)

def open_map(ip_address):
    #ip_address = "103.136.57.191" # example IP address
    location = get_coordinates(ip_address)
    print(location)
    #print(location) # prints "Mountain View, California, US" (location of Google's headquarters)
    display_map(location)


if __name__ == '__main__':
    open_map("103.136.57.191")
    #display_map((-6.2114, 106.8446))



