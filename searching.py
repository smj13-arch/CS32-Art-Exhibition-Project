    #api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0" - Amelie's API
import requests
import requests

def searching_function():
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"
    
    params = {
        "apikey": api_key,
        "size": 10,
        "culture": "Dutch",
        "classification": "Paintings",
        "hasimage": 1,
        "imagepermissionlevel": 0,
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    records = data["records"]

    for i, artwork in enumerate(records, start=1):
        title = artwork.get("title", "Untitled")
        image_url = artwork.get("primaryimageurl")

        if image_url is None:
            print(f"{i}. Skipping (no image): {title}")
            continue

        image_data = requests.get(image_url).content

        filename = f"painting_{i}.jpg"

        with open(filename, "wb") as f:
            f.write(image_data)

        print(f"{i}. Saved: {title}")

    return records

def main():
    searching_function()


main()

