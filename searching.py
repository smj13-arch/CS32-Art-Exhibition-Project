import requests
import os
import random
from PIL import Image
from io import BytesIO

# create "gallery" folder to save images to
GALLERY_DIR = "gallery"
os.makedirs(GALLERY_DIR, exist_ok=True)

def build_html_gallery(artworks, page_title, name):
    if not artworks:
        print("No artworks to build gallery.")
        return

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{page_title}</title>
  <style>
    * {{
      box-sizing: border-box;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      background: #f3f3f3;
      margin: 0;
    }}
    h1 {{
      text-align: center;
      padding: 24px 16px 4px;
      margin: 0;
      font-size: 2.4rem;
    }}
    h2 {{
      text-align: center;
      margin: 0 0 24px;
      font-weight: normal;
      color: #666;
      font-size: 1.1rem;
    }}
    .page {{
      max-width: 900px;
      margin: 0 auto 48px;
      padding: 0 16px 32px;
    }}
    .card {{
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.16);
      overflow: hidden;
      margin: 24px 0;
    }}
    .card img {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .info {{
      padding: 14px 18px 16px;
      font-size: 0.95rem;
      line-height: 1.5;
    }}
    .title {{
      font-weight: 600;
      margin-bottom: 4px;
    }}
    .artist {{
      font-style: italic;
      color: #444;
    }}
    .year {{
      color: #777;
      margin-top: 2px;
      margin-bottom: 8px;
    }}
    .meta {{
      color: #555;
      margin-top: 4px;
      font-size: 0.9rem;
    }}
    .description {{
      color: #555;
      margin-top: 4px;
    }}
  </style>
</head>
<body>
  <h1>{name}'s Art Exhibition</h1>
  <h2>{page_title}</h2>
  <div class="page">
"""

    for art in artworks:
        src = f"{GALLERY_DIR}/{art['filename']}"
        title = art["title"]
        artist = art["artist"]
        year = art["year"]
        culture = art.get("culture", "Unknown Culture")
        classification = art.get("classification", "Unknown Classification")
        medium = art.get("medium", "Unknown Medium")
        technique = art.get("technique", "Unknown Technique")
        description = art.get("description", "")

        html += f"""    <div class="card">
      <img src="{src}" alt="{title}">
      <div class="info">
        <div class="title">{title}</div>
        <div class="artist">{artist}</div>
        <div class="year">{year}</div>
        <div class="meta">
          <strong>Culture:</strong> {culture}<br>
          <strong>Classification:</strong> {classification}<br>
          <strong>Medium:</strong> {medium}<br>
          <strong>Technique:</strong> {technique}
        </div>"""

        if description:
            html += f"""
        <div class="description">{description}</div>"""

        html += """
      </div>
    </div>
"""

    html += """  </div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Gallery written to index.html – open it in your browser by running open index.html in the terminal.")


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

    medium = input("Medium - e.g.: Watercolor, Bronze, Oil (optional): ").strip()
    medium = medium[0].upper() + medium[1:] if medium else medium

    technique = input("Technique - e.g.: Etching, Cast, Woodcut (optional): ").strip()
    technique = technique[0].upper() + technique[1:] if technique else technique

    keyword = input("Keyword/theme - e.g. love, blue (optional): ").strip()
    keyword = keyword[0].upper() + keyword[1:] if keyword else keyword

    print()
    return title, start_year, end_year, artist, culture, classification, medium, technique, keyword


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


def searching_function(
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
        existing_artworks = []

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

    response = requests.get(base_url, params=params)
    data = response.json()
    records = data.get("records", [])

    if not records:
        print("No artworks found matching your search criteria.")
        return existing_artworks

    saved_count = len(existing_artworks)

    for artwork in records:
        if saved_count >= target_count:
            break
        saved = save_artwork_to_gallery(artwork, saved_count)
        if saved:
            existing_artworks.append(saved)
            saved_count += 1

    return existing_artworks


def random_fill(artworks, target_count=5):
    base_url = "https://api.harvardartmuseums.org/object"
    api_key = "d085cac8-e2aa-425f-b3d5-2c5b49d15fc0"

    saved_count = len(artworks)

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
            saved = save_artwork_to_gallery(artwork, saved_count, label=" (random)")
            if saved:
                artworks.append(saved)
                saved_count += 1

    return artworks

def build_criteria_string(title, start_year, end_year, artist, culture, classification, medium, technique, keyword):
    parts = []

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

    # join nicely: "A, B, and C"
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]

def main():

    # delete any old artwork files in gallery
    for f in os.listdir(GALLERY_DIR):
        if f.lower().startswith("artwork_") and f.lower().endswith(".jpg"):
            os.remove(os.path.join(GALLERY_DIR, f))

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
