    #api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0" - Amelie's API
import requests
import requests

def searching_function():
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"
    import requests

    params = {
        "apikey": api_key,
        "size": 10,
        "classification": "Paintings",
        "hasimage": 1,
        "imagepermissionlevel": 0,
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    records = data["records"]

    saved_count = 0
    for artwork in records:
        title = artwork.get("title", "Untitled")
        image_url = artwork.get("primaryimageurl")

        if image_url is None:
            print(f"Skipping (no image): {title}")
            continue

        saved_count += 1
        image_data = requests.get(image_url).content

        with open(f"painting_{saved_count}.jpg", "wb") as f:
            f.write(image_data)

        print(f"{saved_count}. Saved: {title}")

    print(f"\nDone! Saved {saved_count} paintings.")

def main():
    searching_function()

main()

def main():
    searching_function()


main()

