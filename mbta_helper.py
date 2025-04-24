#---------------------------------------------
# Step 1: Accessing Web Data Programmatically:
#---------------------------------------------

import json
import os
import pprint
import urllib.request
import urllib.parse

from dotenv import load_dotenv

# Load environment variables from .env file (contains the API Keys)
load_dotenv()

# Get API keys from environment variables:
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# print("MAPBOX_TOKEN", MAPBOX_TOKEN)
# print("MBTA_API_KEY", MBTA_API_KEY)

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

#--------------------------------------------
#Helper Functions:
#--------------------------------------------

def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    with urllib.request.urlopen(url) as response:
    # Opens the URL and assignts the response as 'response'.
        return json.load(response)
    # Returns the JSON data from the response, and delivers the output into a Python dictionary. 

def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    encoded_place = urllib.parse.quote(place_name)
    # Encodes the place name to ensure that the URL is accurate based on location inputted by the user. 
    url = f"{MAPBOX_BASE_URL}/{encoded_place}.json?access_token={MAPBOX_TOKEN}"
    # Creates the Mapbox API URL, taking the place (location) that is now encoded successfully, and the Mapbox API token. 
    
    data = get_json(url)

    print("Mapbox response:", data)

    if not data ["features"]:
        raise ValueError(
            f"No results were found for '{place_name}'. Please check the spelling or try a different place."
        )
    # Finally, we call the get_json() function to return the JSON data sufficiently into Python. 

    # Mapbox returns the coordinates as [longitude, latitude]
    longitude, latitude = data["features"][0]["center"]

    return str(latitude), str(longitude)
    # Return latitude and longitude as strings - latitude first, longitude next. 

def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance"
    # Creates the MBTA API URL, taking the latitude and longitude and the MBTA API key,
    # whilst sorting results by distance.

    data = get_json(url) # Call the get_json() function to return the JSON data from the MBTA API sufficiently into Python. 
    stop = data["data"][0] # Retrieve the first stop in the 'data' key list, which returns the closest stop based on inputted location.
    station_name = stop["attributes"]["name"] # Returns the station name from the 'attributes' dictionary of the stop.
    wheelchair_code = stop["attributes"]["wheelchair_boarding"] 
    # Gets the wheelchair boarding code: 1 = accessible, 2 = not accessible, 0 = no info.

    wheelchair_accessible = wheelchair_code == 1 
    # To see if there is wheelchair accessibility, by seeing if the code is 1 (True). If anything else, false otherwise. 
    return station_name, wheelchair_accessible
    # Returns the station name, and whether it is wheelchair accessible, as a tuple.


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    lat, lng = get_lat_lng(place_name)
    # Calls the get_lat_lng() function to get the latitude and longitude of the place inputted by the user.
    return get_nearest_station(lat, lng)
    # Calls the get_nearest_station() function to analyze the above given coordinates, and returns
    # the nearest MBTA stop and its status of wheelchair accessibility. 

#-----------------------------------------
# Step 2: Structured Data Responses (JSON)
#-----------------------------------------

# Taking written code from Step 2, to print the JSON structure:
from dotenv import load_dotenv

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"

query = "Babson College"
query = query.replace(" ", "%20") # In URL encoding, spaces are typically replaced with "%20". Can also use `urllib.parse.quote` function. 
url=f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi"
print(url) # Try this URL in your browser first

with urllib.request.urlopen(url) as resp:
    response_text = resp.read().decode("utf-8")
    response_data = json.loads(response_text)
    pprint.pprint(response_data)

# Created Function To Extract Latitude and Longitude From JSON Response:
def extract_lat_lng(response_data):
    """
    As a result of the JSON Response from Mapbox, extract the
    latitude and longitude (latitude, longitude) for Babson College.

    Returns the (latitude, longitude) as a tuple.
    """

    feature = response_data["features"[0]]
    # 'feature' is a list of potential matching locations returned by Mapbox.
    # [0] retrieves the first match that is most relevant from the 'feature' list.
    # The first match/feature is used as the best match for the inputted query, 'Babson College'. 
    longitude, latitude = feature["center"]
    # Each feature contains a 'center' key that has the stored coordinates. 
    # 'center' is another list that stores coordinates in the form of: [longitude, latitude] as
    # Mapbox always gives longitude first then latitude from its responses.

    return latitude, longitude
    # Returns the latitude and longitude as a tuple in the normal, required (latitude, longitude) order. 

# Testing The New Function:
# def main():
#     lat, lng = extract_lat_lng(response_data) 
#     # Get the response_data and call the new extract_lat_lng function. 
#     # Store the results in 'lat' and 'lng'. 
#     print("Latitude:", lat) # Prints the latitude value. 
#     print("Longitude", lng) # Prints the longitude value.

# if __name__ == "__main__":
#     main()

#------------------------
# Step 3: Building A URL:
#------------------------

from urllib.parse import quote

def build_mapbox_geocoding_url(place_name, mapbox_token):
    """
    Build a proper econded URL for a Mapbox Geocoding request.

    place_name (str): The location, place name or address to geocode.
    mapbox_token (str): Personal Mapbox API token created. 
    """

    # Encode the place name, so that it is safe and accurately used in a URL.
    # Example: "Boston Common" will become, "Boston%20Common"
    encoded_place = quote(place_name)

    # Create the full URL for a Mapbox Geocoding Request:
    # Scheme = 'https'
    # Authority = 'api.mapbox.com'
    # The Path includes the encoded place name, ending with '.json'.
    # The query

    url = (f"https://api.mapbox.com/geocoding/v5/mapbox.places/"
           f"{encoded_place}.json?access_token={mapbox_token}&types=poi"
    )

    return url 
    # Return the created URL as a string. 

#-----------------------
# Step 4: Getting Local:
#-----------------------

# Use previous written helper function: get_nearest_station. 

def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    latitude (str): The latitude of the location/place. 
    longitude (str): The longitude of the location/place.

    Returned Output:
    tuple: (station_name, wheelchair_accessible)
    
    station_name (str): Name of the nearest MBTA stop.
    wheelchair_accessible (bool): Returns True if wheelchair accessible, False if not. 
    """

    # Using the given latitude and longitude, and the MBTA API Key, build the MBTA API URL:
    # The 'sort=distance' parameter ensures the closest stop for the inputted location is first in the results.
    url = (
        f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}"
        f"&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance"
    )

    # Example URL For Boston Common:
    # https://api-v3.mbta.com/stops?api_key=YOUR_KEY&filter[latitude]=42.3550&filter[longitude]=-71.0656&sort=distance

    # To get the appropriate JSON Response from the MBTA API, use part of previous helper function:
    # data = get_json(url)

    data = get_json(url)

    stop = data["data"][0] 
    # Retrieve the first stop in the 'data' key list, which returns the closest stop based on inputted location.

    station_name = stop["attributes"]["name"] # Returns the station name from the 'attributes' dictionary of the stop.
    wheelchair_code = stop["attributes"]["wheelchair_boarding"] 
    # Gets the wheelchair boarding code: 1 = accessible, 2 = not accessible, 0 = no info.

    wheelchair_accessible = wheelchair_code == 1 
    # To see if there is wheelchair accessibility, by seeing if the code is 1 (True). If anything else, false otherwise. 
    return station_name, wheelchair_accessible
    # Returns the station name, and whether it is wheelchair accessible, as a tuple.

#--------------------
# Step 5: To Wrap Up:
#--------------------

def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Once a place name/address is given:

    Step 1: Find the latitude and longitude of the place using the Mapbox API.
    Step 2: Find the nearest MBTA stop for those coordinates using the MBTA API.
    Step 3: Return the name of the nearest MBTA stop and whether it is wheelchair accessible.

    place_name (str): The address or place name inputted by the user. 

    Returned Output:
    tuple: (station_name, wheelchair_accessible)
    
    station_name (str): Name of the nearest MBTA stop.
    wheelchair_accessible (bool): Returns True if wheelchair accessible, False if not. 
    """

    # Find the latitude and longitude of the place using the Mapbox API.
    latitude, longitude = get_lat_lng(place_name)
    # The get_lat_lng() function helps to return the (latitude, longitude) as strings.

    # Find the nearest MBTA stop for those coordinates using the MBTA API.
    station_name, wheelchair_accessible = get_nearest_station(latitude, longitude)
    # The get_nearest_station() function helps to return the closest station name, and if it is wheelchair accessible.

    # Return the result(name of the nearest MBTA stop and whether it is wheelchair accessible)
    return station_name, wheelchair_accessible

#-----------------------------------------
# Main Test Of The Above Functions & Steps:
#-----------------------------------------

def main():
    """
    You should test all the above functions here.
    """
    place = "Boston Common" # Inputting a place name for test. 
    station, accessible = find_stop_near(place) # Calls find_stop_near() function to get nearest station and wheelchair accessibility. 
    print(f"Nearest MBTA Station to {place}: {station}") # Prints the nearest station's name.
    print(f"Wheelchair accessible: {'Yes' if accessible else 'No'}") # Prints if the station is or is not wheelchair accessible.

if __name__ == "__main__":
    main()

