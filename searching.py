import requests
import os
import random
from PIL import Image
from io import BytesIO


def client():
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
    return title, start_year, end_year, artist, culture, classification, keyword


def save_artwork(artwork, saved_count, label=""):
    image_url = artwork.get("primaryimageurl")
    if not image_url:
        return False

    art_title = artwork.get("title", "Untitled")
    art_artist = artwork.get("people", [{}])[0].get("name", "Unknown Artist") if artwork.get("people") else "Unknown Artist"
    art_year = artwork.get("dated", "Unknown Year")
    art_culture = artwork.get("culture", "Unknown Culture")
    art_classification = artwork.get("classification", "Unknown Classification")

    img_response = requests.get(image_url)
    content_type = img_response.headers.get("Content-Type", "")

    if "image" not in content_type:
        return False

    image = Image.open(BytesIO(img_response.content))
    if image.mode != "RGB":
        image = image.convert("RGB")
    filename = f"artwork_{saved_count + 1}.jpg"
    image.save(filename, "JPEG")
    print(f"Saved {filename}{label}")
    print("  Title:", art_title)
    print("  Artist:", art_artist)
    print("  Year:", art_year)
    print("  Culture:", art_culture)
    print("  Classification:", art_classification)
    print()
    return True


def searching_function(title="", start_year="", end_year="", artist="", culture="", classification="", keyword="", saved_count=0, target_count=5):
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"

    params = {
        "apikey": api_key,
        "size": 30,
        "hasimage": 1,
        "imagepermissionlevel": 0,
    }

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
        return saved_count

    for artwork in records:
        if saved_count >= target_count:
            break
        if save_artwork(artwork, saved_count):
            saved_count += 1

    return saved_count


def random_fill(saved_count, target_count=5):
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"

    while saved_count < target_count:
        random_page = random.randint(1, 500)
        params = {
            "apikey": api_key,
            "size": 30,
            "hasimage": 1,
            "imagepermissionlevel": 0,
            "page": random_page,
        }

        response = requests.get(base_url, params=params)
        data = response.json()
        records = data.get("records", [])
        random.shuffle(records)

        for artwork in records:
            if saved_count >= target_count:
                break
            if save_artwork(artwork, saved_count, label=" (random)"):
                saved_count += 1

    return saved_count


def main():
    print("Harvard Art Museums Search")
    print("Leave any field blank to skip that filter.\n")

    title, start_year, end_year, artist, culture, classification, keyword = client()

    for i in range(1, 6):
        filename = f"artwork_{i}.jpg"
        if os.path.exists(filename):
            os.remove(filename)

    target_count = 5
    saved_count = searching_function(
        title=title, start_year=start_year, end_year=end_year,
        artist=artist, culture=culture, classification=classification,
        keyword=keyword, target_count=target_count,
    )

    while saved_count < target_count:
        print(f"We only found {saved_count} artwork(s) so far and we require that our exhibitions are five pieces. What would you like to do?")
        choice = input("Would you like to (1) randomly generate the rest, or (2) search again with new parameters? Enter 1 or 2: ").strip()
        print()

        if choice == "1":
            saved_count = random_fill(saved_count, target_count)
            break
        elif choice == "2":
            title, start_year, end_year, artist, culture, classification, keyword = client()
            saved_count = searching_function(
                title=title, start_year=start_year, end_year=end_year,
                artist=artist, culture=culture, classification=classification,
                keyword=keyword, saved_count=saved_count, target_count=target_count,
            )
        else:
            print("Invalid choice. Please enter 1 or 2.\n")

    for i in range(1, 6):
        filename = f"artwork_{i}.jpg"
        if os.path.exists(filename):
            Image.open(filename).show()


main()
