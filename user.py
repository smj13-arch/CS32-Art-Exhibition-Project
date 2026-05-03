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

    return name


