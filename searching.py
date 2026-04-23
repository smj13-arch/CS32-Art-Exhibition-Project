
import random
import requests

def searching_function(start_time, end_time, artist, country, material):
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"

    params = {
        "apikey": api_key,
        "size": 10,
        "q": f"datebegin:[{start_time} TO {end_time}] AND people.name:{artist} AND culture:{country} AND medium:{material}"
    }   

