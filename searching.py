import requests
from PIL import Image
from io import BytesIO

def searching_function(painting_name):
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"

    params = {
        "apikey": api_key,
        "size": 10,  # get a few results so we can pick the first valid one
        "classification": "Paintings",
        "hasimage": 1,
        "imagepermissionlevel": 0,  # 0 = no restrictions (copyright-free/CC0)
        "title": painting_name     # search by painting title (your parameter)
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    records = data.get("records", [])
    if not records:
        print(f"No paintings found matching '{painting_name}'.")
        return

    # Loop through results and grab the FIRST painting with a usable image
    for artwork in records:
        image_url = artwork.get("primaryimageurl")
        if not image_url:
            continue  # skip if no image

        title = artwork.get("title", "Untitled")
        artist = artwork.get("people", [{}])[0].get("name", "Unknown Artist")
        year = artwork.get("dated", "Unknown Year")

        print("Title:", title)
        print("Artist:", artist)
        print("Year:", year)

        img_response = requests.get(image_url)
        content_type = img_response.headers.get("Content-Type", "")

        if "image" in content_type:
            image_data = img_response.content

            # Open the image with PIL
            image = Image.open(BytesIO(image_data))

            # Convert to RGB so we can save as JPG (JPG doesn't support RGBA/P modes)
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Save as a proper JPG file
            image.save("painting.jpg", "JPEG")
            print("Saved as painting.jpg")

            image.show()
            return  # stop after first valid painting

        else:
            print("Could not load image for this record. Trying next...")
            print("Returned type:", content_type)

    print("No paintings with usable images were found.")


def main():
    # Pass any painting title here as the parameter
    searching_function("Sunset")

main()
