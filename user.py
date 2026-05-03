# Instructions and welcome user to ART EXHIBITOR
from searching import delete_old_artwork_files
from searching import client
from searching import searching_function
from searching import random_fill
from searching import build_criteria_string
from website import build_html_gallery
import os
from website import save_artwork_to_gallery

def user():
    intro_text = """
    ### Welcome to ART EXHIBITOR: Dream Gallery ###

    We are excited to provide you a tool to help visualize your dream art gallery,
    using pieces from our very own Harvard Art Museums! To get started, either provide
    specific search parameters to gather the pieces you've been dreaming of, but couldn't
    quite name--or leave it up to us and generate a random virtual gallery.

    We have the capacity to create virtual galleries of 5 pieces, including short title
    cards and descriptions beneath each piece. Happy curating! :D
    """

    print(intro_text) # utilizing multiline print statement

    print("Let's begin!")
    name = input("What's your name? ").strip()
    print(f"Perfect! Let's create {name}'s Art Exhibition:\n")
    note = """
    To start curating your own gallery, enter your search criteria below. You can specify
    as many or as few as you'd like! Also, if you're unsure about any of the search criteria,
    you can either leave the field blank or take a look at the Harvard Art Museums' available
    selections in search_options.md for some inspiration. We hope this search tool suits
    your artistic fancy!
    """
    print(note)


def main():

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


