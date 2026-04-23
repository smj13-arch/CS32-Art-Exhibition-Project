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
        "imagepermissionlevel": 0
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    artwork = data["records"][0]

    title = artwork.get("title", "Untitled")
    artist = artwork.get("people", [{}])[0].get("name", "Unknown Artist")
    year = artwork.get("dated", "Unknown Year")
    image_url = artwork.get("primaryimageurl")

    print("Title:", title)
    print("Artist:", artist)
    print("Year:", year)

    if image_url:
        img_response = requests.get(image_url)

        content_type = img_response.headers.get("Content-Type", "")

        if "image" in content_type:
            image_data = img_response.content

            with open("painting.jpg", "wb") as f:
                f.write(image_data)

            image = Image.open(BytesIO(image_data))
            image.show()

        else:
            print("Could not load image.")
            print("Returned type:", content_type)

    else:
        print("No image found.")

def main():
    searching_function()

main()
