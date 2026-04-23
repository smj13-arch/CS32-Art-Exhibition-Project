    #api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0" - Amelie's API
import requests

def searching_function():
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"

    params = {
        "apikey": api_key,
        "size": 1,
        "classification": "Paintings",
        "hasimage": 1,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    artwork = data["records"][0]
    image_url = artwork.get("primaryimageurl")
    title = artwork.get("title", "Untitled")

    if image_url is None:
        print(f"No image available for: {title}")
        return artwork

    image_data = requests.get(image_url).content

    with open("painting.jpg", "wb") as f:
        f.write(image_data)

    print(f"Saved: {title}")

    return artwork
