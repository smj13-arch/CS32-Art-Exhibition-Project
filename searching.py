import requests
import os
from PIL import Image
from io import BytesIO

def searching_function(title="", start_year="", end_year="", artist="", culture="", classification="", keyword=""):
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"

    # Build params dictionary - only include non-empty values
    params = {
        "apikey": api_key,
        "size": 30,
        "hasimage": 1,
        "imagepermissionlevel": 0,
    }

    # Add optional parameters only if they're not empty
    if title:
        params["title"] = title
    if artist:
        params["person"] = artist
    if culture:
        params["culture"] = culture
    if classification:
        params["classification"] = classification
    if keyword:
        params["keyword"] = keyword

    # Handle year range - the API uses "yearmade" with a range format
    if start_year and end_year:
        params["yearmade"] = f"{start_year}-{end_year}"
    elif start_year:
        params["yearmade"] = f"{start_year}-2026"
    elif end_year:
        params["yearmade"] = f"0-{end_year}"

    response = requests.get(base_url, params=params)
    data = response.json()
    records = data.get("records", [])

    if not records:
        print("No artworks found matching your search criteria.")
        return

    saved_count = 0
    target_count = 5

    for artwork in records:
        if saved_count >= target_count:
            break
        image_url = artwork.get("primaryimageurl")
        if not image_url:
            continue

        art_title = artwork.get("title", "Untitled")
        art_artist = artwork.get("people", [{}])[0].get("name", "Unknown Artist") if artwork.get("people") else "Unknown Artist"
        art_year = artwork.get("dated", "Unknown Year")
        art_culture = artwork.get("culture", "Unknown Culture")
        art_classification = artwork.get("classification", "Unknown Classification")

        img_response = requests.get(image_url)
        content_type = img_response.headers.get("Content-Type", "")

        if "image" in content_type:
            image_data = img_response.content
            image = Image.open(BytesIO(image_data))
            if image.mode != "RGB":
                image = image.convert("RGB")
            filename = f"artwork_{saved_count + 1}.jpg"
            image.save(filename, "JPEG")
            print(f"Saved {filename}")
            print("  Title:", art_title)
            print("  Artist:", art_artist)
            print("  Year:", art_year)
            print("  Culture:", art_culture)
            print("  Classification:", art_classification)
            print()
            saved_count += 1
        else:
            print("Could not load image for this record. Trying next...")

    if saved_count == 0:
        print("No artworks with usable images were found.")
    elif saved_count < target_count:
        print(f"Only found {saved_count} usable artworks (wanted {target_count}).")


def main():
    print("Harvard Art Museums Search")
    print("Leave any field blank to skip that filter.\n")

    title = input("Title (optional): ").strip()
    start_year = input("Start year (optional): ").strip()
    end_year = input("End year (optional): ").strip()
    artist = input("Artist (optional): ").strip()
    artist = artist[0].upper() + artist[1:] if artist else artist

    culture = input("Culture (optional): ").strip()
    culture = culture[0].upper() + culture[1:] if culture else culture

    classification = input("Classification - e.g.: Sculpture, Painting (optional): ").strip()
    classification = classification[0].upper() + classification[1:] if classification else classification

    keyword = input("Keyword/theme - e.g. love, blue (optional): ").strip()
    keyword = keyword[0].upper() + keyword[1:] if keyword else keyword

    print()

    # delete any old artwork files (we only want to focus on the new search results)
    for i in range(1, 6):
        filename = f"artwork_{i}.jpg"
        if os.path.exists(filename):
            os.remove(filename)

    searching_function(
        title=title,
        start_year=start_year,
        end_year=end_year,
        artist=artist,
        culture=culture,
        classification=classification,
        keyword=keyword
    )

    for i in range(1, 6):
        filename = f"artwork_{i}.jpg"
        if os.path.exists(filename):
            Image.open(filename).show()


main()
