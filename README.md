# cs32-project

Welcome to the ART EXHIBITOR! (by Amelie Chen and Sirja Jõeveer)

This is our final project for CS32. Drawing upon Sirja's freshman seminar in the Harvard Art Museums,
where she visited the museums every week for class, we realized the difficulty of creating and developing
art galleries. It is often infeasible to physically find the art pieces and lay them out without spending
hours, days, or even weeks finding orientations that are both aesthetically pleasing and agree with
the artists' intentions.

## What our project does

Essentially, the ART EXHIBITOR allows users to generate and visualize their own art galleries, drawing upon
a wide selection from the Harvard Art Museums' collection. We utilize the Harvard Art Museums API (we obtained
a personal key for this project) to parse through artworks and find five pieces which match the user's search
query. An additional component we added to this project was the ability to paste the images of the art pieces to
a a live HTML web link (it was quite difficult, so we utilized generative AI to help us accomplish this). It links
the pieces to a web page, with information such as title, year, medium, and the piece description displayed as well.

## Instructions for Running the Code

To start the program, run the command "python3 searching.py" in your terminal from the project folder:
> ⚠️ **Note:** This program will not work on CS50.dev — it must be run locally (e.g. VS Code on desktop).
This launches the `main()` function inside `searching.py`, which starts the Harvard Art Museums Curation tool.

From there, the program will:
1. Ask for your name to customize your very own Art Exhibit
2. For inspiration on what to search, browse through `searching_options.md` — open it in preview mode with **Cmd + Shift + V** (Mac) or **Ctrl + Shift + V** for a nice formatted view.
3. Collect search parameters one at a time: title, start year, end year, artist, culture, classification, medium, technique, and keyword/theme. All fields are optional; leave any blank to skip that filter.
4. Query the Harvard Art Museums API to assemble a gallery of 5 artworks based on your criteria.
5. Generate a `index.html` file to create your dream art gallery!

## Special steps

In order for this project to work, we quickly realized (with guidance from our wonderful amazing glorious TA Adrian) that
simply pasting the data from the Harvard Art Museums website into a CSV file would not be feasible. Instead, we learned how
to work with the capabilities of the Harvard Art Museums API and leveraged its resources to make this project a reality! For
example, we requested to get our own personal API key, downloaded JSON reader extensions to chrome in the early stages of
understanding our data, and finally used the aid of generative AI to help get the data from the API to the webpage.





