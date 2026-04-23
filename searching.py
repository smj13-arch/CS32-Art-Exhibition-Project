    #api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0" - Amelie's API
import requests
from PIL import Image
from io import BytesIO

def searching_function():
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"

    params = {
        "apikey": api_key,
        "size": 1,
        "classification": "Paintings",
        "hasimage": 1,
        "imagepermissionlevel": 0,
        "sort": "rank",
        "sortorder": "asc",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    artwork = data["records"][0]
    title = artwork.get("title", "Untitled")
    image_url = artwork.get("primaryimageurl")

    print(f"Title: {title}")
    print(f"Image URL: {image_url}")

    image_data = requests.get(image_url).content

    with open("painting.jpg", "wb") as f:
        f.write(image_data)

    image = Image.open(BytesIO(image_data))
    image.show()

def main():
    searching_function()


main()

