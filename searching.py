import requests
import os
import random
from PIL import Image
from io import BytesIO
from website import build_html_gallery

# create gallery folder to save images to
GALLERY_DIR = "gallery"
os.makedirs(GALLERY_DIR, exist_ok=True)


def client():
    #getting information from our client/user to use as search parameters for the API search
    title = input("Title (optional): ").strip()
    start_year = input("Start year (optional): ").strip()
    end_year = input("End year (optional): ").strip()
    artist = input("Artist (optional): ").strip()
    artist = artist[0].upper() + artist[1:] if artist else artist
    #it was case-sensitive, so we made sure that every first letter was capitlized

    culture = input("Culture (optional): ").strip()
    culture = culture[0].upper() + culture[1:] if culture else culture

    classification = input("Classification - e.g.: Sculpture, Painting (optional): ").strip()
    classification = classification[0].upper() + classification[1:] if classification else classification

    medium = input("Medium - e.g.: Watercolor, Bronze, Oil (optional): ").strip()
    medium = medium[0].upper() + medium[1:] if medium else medium

    technique = input("Technique - e.g.: Etching, Cast, Woodcut (optional): ").strip()
    technique = technique[0].upper() + technique[1:] if technique else technique

    keyword = input("Keyword/theme - e.g. love, blue (optional): ").strip()
    keyword = keyword[0].upper() + keyword[1:] if keyword else keyword

    print()
    return title, start_year, end_year, artist, culture, classification, medium, technique, keyword


def searching_function( #The quotations were added so that the entry was optional—some entries could be empty
    title="",
    start_year="",
    end_year="",
    artist="",
    culture="",
    classification="",
    medium="",
    technique="",
    keyword="",
    existing_artworks=None,
    target_count=5,
):
    if existing_artworks is None:
        existing_artworks = [] #in the case our search returns fewer than 5 pieces, we save the first few pieces
    # search the Harvard Art Museums API - we got the API key from the website/documentation
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"

    params = {
        "apikey": api_key,
        "size": 30, #were pulling up the first thirty
        "hasimage": 1, #making sure it has an image since many have copy right issues
        "imagepermissionlevel": 0, # using public domain
    }

    if title:
        params["title"] = title
    if artist:
        params["person"] = artist
    if culture:
        params["culture"] = culture
    if classification:
        params["classification"] = classification
    if medium:
        params["medium"] = medium
    if technique:
        params["technique"] = technique
    if keyword:
        params["keyword"] = keyword

    if start_year and end_year:
        params["yearmade"] = f"{start_year}-{end_year}"
    elif start_year:
        params["yearmade"] = f"{start_year}-2026"
    elif end_year:
        params["yearmade"] = f"0-{end_year}"

    response = requests.get(base_url, params=params) # seting up our requests
    data = response.json() # storing the data
    records = data.get("records", [])

    if not records: # if we don't find anything
        print("No artworks found matching your search criteria.")
        return existing_artworks

    saved_count = len(existing_artworks) # counts how many artworks we've already saved

    for artwork in records:
        if saved_count >= target_count:
            break # whenever we've gotten past 5, just stop this loop entirely
        saved = save_artwork_to_gallery(artwork, saved_count) # call function to save artworks to gallery
        if saved:
            existing_artworks.append(saved) # add saved artwork to our list of existing artworks
            saved_count += 1 # counter

    return existing_artworks #return the artworks our search found!


def random_fill(artworks, target_count=5): # function to randomly generate the next paintings (if search returned fewer than 5 or if user requested random gallery)
    base_url = "https://api.harvardartmuseums.org/object" # base url for our API search
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0" # our unique key, requested from Harvard Art Musuem (HAM)

    saved_count = len(artworks)

    while saved_count < target_count:
        random_page = random.randint(1, 500)
        params = {
            "apikey": api_key,
            "size": 30, # searching for 30 pieces at a time to increase our chances of finding something that fits the criteria
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
            saved = save_artwork_to_gallery(artwork, saved_count, label=" (random)")
            if saved:
                artworks.append(saved)
                saved_count += 1

    return artworks


def save_artwork_to_gallery(artwork, saved_count, label=""):
    image_url = artwork.get("primaryimageurl")
    if not image_url:
        return None

    title = artwork.get("title", "Untitled")
    artist = artwork.get("people", [{}])[0].get("name", "Unknown Artist") if artwork.get("people") else "Unknown Artist"
    year = artwork.get("dated", "Unknown Year")
    culture = artwork.get("culture", "Unknown Culture")
    classification = artwork.get("classification", "Unknown Classification")
    medium = artwork.get("medium", "Unknown Medium")
    technique = artwork.get("technique", "Unknown Technique")
    description = artwork.get("description") or artwork.get("labeltext") or ""

    img_response = requests.get(image_url)
    content_type = img_response.headers.get("Content-Type", "")

    if "image" not in content_type:
        return None

    image = Image.open(BytesIO(img_response.content))
    if image.mode != "RGB":
        image = image.convert("RGB")

    filename = os.path.join(GALLERY_DIR, f"artwork_{saved_count + 1}.jpg")
    image.save(filename, "JPEG")
    #printing out data about the pieces we just saved to the gallery
    print(f"Saved {filename}{label}")
    print("  Title:", title)
    print("  Artist:", artist)
    print("  Year:", year)
    print("  Culture:", culture)
    print("  Classification:", classification)
    print("  Medium:", medium)
    print("  Technique:", technique)
    print()

    return {
        "filename": os.path.basename(filename),
        "title": title,
        "artist": artist,
        "year": year,
        "culture": culture,
        "classification": classification,
        "medium": medium,
        "technique": technique,
        "description": description,
    }

# generated by AI for the website building HTML (this gives the caption beneath the Art Exhibition)
def build_criteria_string(title, start_year, end_year, artist, culture, classification, medium, technique, keyword):
    parts = []
    # building the search criteria based on the user's input, which will be displayed on the webpage as part of the title of the gallery
    if title:
        parts.append(f'title "{title}"')
    if artist:
        parts.append(f'artist "{artist}"')
    if culture:
        parts.append(f'culture "{culture}"')
    if classification:
        parts.append(f'classification "{classification}"')
    if medium:
        parts.append(f'medium "{medium}"')
    if technique:
        parts.append(f'technique "{technique}"')
    if keyword:
        parts.append(f'keyword "{keyword}"')
    if start_year and end_year:
        parts.append(f'year range {start_year}–{end_year}')
    elif start_year:
        parts.append(f'year ≥ {start_year}')
    elif end_year:
        parts.append(f'year ≤ {end_year}')

    if not parts:
        return "a random selection"
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]

def delete_old_artwork_files():
        # delete any old artwork files in gallery
    for f in os.listdir(GALLERY_DIR):
        if f.lower().startswith("artwork_") and f.lower().endswith(".jpg"):
            os.remove(os.path.join(GALLERY_DIR, f))


def main():
    intro_text = """
    ### Welcome to ART EXHIBITOR: Dream Gallery ###

    We are excited to provide you a tool to help visualize your dream art gallery,
    using pieces from our very own Harvard Art Museums! To get started, either provide
    specific search parameters to gather the pieces you've been dreaming of, but couldn't
    quite name--or leave it up to us to generate a random virtual gallery.

    We currently have the capacity to create virtual galleries of 5 pieces, including
    short title cards and descriptions beneath each piece. Happy curating! :D
    """

    print(intro_text) # utilizing multiline print statement
    name = input("What's your name? ").strip()
    print(f"Perfect! Let's create {name}'s Art Exhibition:\n")
    print("Let's begin!")

    note = """
    To start curating your own gallery, enter your search criteria below. You can specify
    as many or as few as you'd like! Also, if you're unsure about any of the search criteria,
    you can either leave the field blank or take a look at the Harvard Art Museums' available
    selections in search_options.md for some inspiration. Note: if you do not enter anything,
    your gallery will be randomly generated. We hope this search tool suits your artistic fancy!
    """
    print(note)

    delete_old_artwork_files()

    title, start_year, end_year, artist, culture, classification, medium, technique, keyword = client()
    target_count = 5
    artworks = searching_function(
        title=title,
        start_year=start_year,
        end_year=end_year,
        artist=artist,
        culture=culture,
        classification=classification,
        medium=medium,
        technique=technique,
        keyword=keyword,
        existing_artworks=[],
        target_count=target_count,
    )

    while len(artworks) < target_count:
        print(f"We only found {len(artworks)} artwork(s) so far and we require that our exhibitions are five pieces. What would you like to do?")
        choice = input("Would you like to (1) randomly generate the rest, or (2) search again with new parameters? Enter 1 or 2: ").strip()
        print()

        if choice == "1":
            artworks = random_fill(artworks, target_count)
            break
        elif choice == "2":
            title, start_year, end_year, artist, culture, classification, medium, technique, keyword = client()
            artworks = searching_function(
                title=title,
                start_year=start_year,
                end_year=end_year,
                artist=artist,
                culture=culture,
                classification=classification,
                medium=medium,
                technique=technique,
                keyword=keyword,
                existing_artworks=artworks,
                target_count=target_count,
            )
        else:
            print("Invalid choice. Please enter 1 or 2.\n")

    # Build HTML gallery with metadata (including culture, classification, medium, technique)
    criteria_str = build_criteria_string(
        title, start_year, end_year, artist, culture, classification, medium, technique, keyword
    )
    page_title = f"{name}'s art gallery based on {criteria_str}"
    build_html_gallery(artworks, page_title, name)


if __name__ == '__main__':
    main()
