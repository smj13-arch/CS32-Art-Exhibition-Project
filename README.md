# cs32-project

Welcome to the ART EXHIBITOR! (by Amelie Chen and Sirja Jõeveer)

This is our final project for CS32. Drawing upon Sirja's freshman seminar in the Harvard Art Museums,
where she visited the museums every week for class, we realized the difficulty of creating and developing
art galleries. It is often infeasible to physically find the art pieces and lay them out without spending
hours, days, or even weeks finding orientations that are both aesthetically pleasing and agree with
the artists' intentions.


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



