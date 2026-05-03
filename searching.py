import requests
import os
from PIL import Image
from io import BytesIO


def searching_function(painting_name):
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"
    params = {
        "apikey": api_key,
        "size": 30,
        "classification": "Paintings",
        "hasimage": 1,
        "imagepermissionlevel": 0,
        "title": painting_name
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    records = data.get("records", [])
    if not records:
        print(f"No paintings found matching '{painting_name}'.")
        return

    saved_count = 0
    target_count = 5

    for artwork in records:
        if saved_count >= target_count:
            break

        image_url = artwork.get("primaryimageurl")
        if not image_url:
            continue

        title = artwork.get("title", "Untitled")
        artist = artwork.get("people", [{}])[0].get("name", "Unknown Artist")
        year = artwork.get("dated", "Unknown Year")

        img_response = requests.get(image_url)
        content_type = img_response.headers.get("Content-Type", "")
        if "image" in content_type:
            image_data = img_response.content
            image = Image.open(BytesIO(image_data))
            if image.mode != "RGB":
                image = image.convert("RGB")

            filename = f"painting_{saved_count + 1}.jpg"
            image.save(filename, "JPEG")

            print(f"Saved {filename}")
            print("  Title:", title)
            print("  Artist:", artist)
            print("  Year:", year)
            print()

            saved_count += 1
        else:
            print("Could not load image for this record. Trying next...")

    if saved_count == 0:
        print("No paintings with usable images were found.")
    elif saved_count < target_count:
        print(f"Only found {saved_count} usable paintings (wanted {target_count}).")


def main():
    searching_function("blue")
    for i in range(1, 6):
        filename = f"painting_{i}.jpg"
        if os.path.exists(filename):
            Image.open(filename).show()


main()
