# website.py
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

