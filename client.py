from searching import searching_function

print("Hello! Welcome to create your own Art Exhibit!")
name = input("What's your name? ")
print("Hello, " + name + "! Nice to meet you and let's get started!!")

#print("Would you like to search for a specific art piece or style? If so, enter your search word. If not, type none")
#assuming we typed none

print("Great! Let's start with some basic questions to help you find the perfect art piece for your exhibit. ")
print("If at anytime you are unsure of what to answer, just type 'N/A' and we will skip that question. ")
start_time = input("Please enter the start year: ")
end_time = input("Please enter the end year: ")
artist = input("Do you have a preferred artist? or type 'N/A' if none:  ")
country = input("Please enter the culture or country: ")
    #searching for culture and country all together
material = input("Please specify the material: (print, paint,..)")
    #look up material or classification on Harvard website to find different types

def main():
    searching_function()


main()
