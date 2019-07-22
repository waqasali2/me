"""All about IO."""


import json
import os
import requests
import inspect
import sys

# Handy constants
LOCAL = os.path.dirname(os.path.realpath(__file__))  # the context of this file
CWD = os.getcwd()  # The curent working directory
if LOCAL != CWD:
    print("Be careful that your relative paths are")
    print("relative to where you think they are")
    print("LOCAL", LOCAL)
    print("CWD", CWD)


def get_some_details():
    """Parse some JSON.
    In lazyduck.json is a description of a person from https://randomuser.me/
    Read it in and use the json library to convert it to a dictionary.
    Return a new dictionary that just has the last name, password, and the
    number you get when you add the postcode to the id-value.
    TIP: Make sure that you add the numbers, not concatinate the strings.
         E.g. 2000 + 3000 = 5000 not 20003000
    TIP: Keep a close eye on the format you get back. JSON is nested, so you
         might need to go deep. E.g to get the name title you would need to:
         data["results"][0]["name"]["title"]
         Look out for the type of brackets. [] means list and {} means
         dictionary, you'll need integer indeces for lists, and named keys for
         dictionaries.
    """
    json_data = open(LOCAL + "/lazyduck.json").read() #open, opens the file, it can now see all the content, the .read() makes python read the file and return it
    #json file, readable by all coding formats. json stands for js- java script on- object notation 

    data = json.loads(json_data) #json.loads, loads the string.It converts it from a json string to a DICTIONARY,
    #We create dictionaries using the curly brackets {}, we acess data using []

    postId = data["results"][0]["location"]["postcode"] + int(data["results"][0]["id"]["value"]) #the reason we have a zero is because the thingo is in a list [.....] and its of length 1 (as there is only one element in the list(all the vales shown)), therefore we call zero 
    #int() turns the number into an integer, this way we can add the values 

    return {"lastName": data["results"][0]["name"]["last"], "password": data["results"][0]["login"]["password"],
            "postcodePlusID": postId} #the reason we have a zero is because the thingo is in a list and its of length 1, therefore we call zero


def wordy_pyramid():
    """Make a pyramid out of real words.
    There is a random word generator here:
    http://api.wordnik.com/v4/words.json/randomWords?api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5&minLength=10&maxLength=10&limit=1
    The arguments that the generator takes is the minLength and maxLength of the word
    as well as the limit, which is the the number of words.
    Visit the above link as an example.
    Use this and the requests library to make a word pyramid. The shortest
    words they have are 3 letters long and the longest are 20. The pyramid
    should step up by 2 letters at a time.
    Return the pyramid as a list of strings.
    I.e. ["cep", "dwine", "tenoner", ...]
    [
    "cep",
    "dwine",
    "tenoner",
    "ectomeric",
    "archmonarch",
    "phlebenterism",
    "autonephrotoxin",
    "redifferentiation",
    "phytosociologically",
    "theologicohistorical",
    "supersesquitertial",
    "phosphomolybdate",
    "spermatophoral",
    "storiologist",
    "concretion",
    "geoblast",
    "Nereis",
    "Leto",
    ]
    TIP: to add an argument to a URL, use: ?argName=argVal e.g. &minLength=
    """

    pyramid_list = []
    temp = "http://api.wordnik.com/v4/words.json/randomWords?api_key={key}&minLength={min}&maxLength={max}&limit=1"

    i = 3 #we start with 3 as we want the first word to have 3 letters
    key1 = "owpgbi1ig2erl892n1c02dgw2y31hgtxnb4xub3qqq133jhn6"
    bool = True
    
    while True: #essentially an infinite loop
        url = temp.format(key = key1, min = i, max = i) #makes the format
        r = requests.get(url) #this gets information form the url
        if r.status_code != 200: #if r.status codes doesnt not = 200
            continue
        elif(bool == True):
            if r.status_code is 200: #if it is 200 
                store = json.loads(r.text)
                pyramid_list.append(store[0]["word"])
                if i == 20:
                    bool = False #this now tells the program to stop increasing "i" and to now start going in the reverse order as it has reached the peak limit that we want
                    i -= 2 #this is essentially 20-2 = 18 because we wanr it to step down by 2 
                elif 20 - i == 1:
                    i += 1
                else:
                    i+=2 #step up by 2 
        elif(bool == False):
            if r.status_code is 200: #if its all good and working perfectly fine
                store = json.loads(r.text)
                pyramid_list.append(store[0]["word"])
                if i-2 < 3: #If the min/max = i is less than 3 which is the bare minimum break the loop
                    break
                else:
                    i-=2
    return pyramid_list



def pokedex(low=1, high=5):
    """ Return the name, height and weight of the tallest pokemon in the range low to high.
    Low and high are the range of pokemon ids to search between.
    Using the Pokemon API: https://pokeapi.co get some JSON using the request library
    (a working example is filled in below).
    Parse the json and extract the values needed.
    TIP: reading json can someimes be a bit confusing. Use a tool like
         http://www.jsoneditoronline.org/ to help you see what's going on.
    TIP: these long json accessors base["thing"]["otherThing"] and so on, can
         get very long. If you are accessing a thing often, assign it to a
         variable and then future access will be easier.
    """
    template = "https://pokeapi.co/api/v2/pokemon/{id}"

    tmp_dict = {
        "name" : None,
        "weight" : None,
        "height" : None
    } #here we have created a dictionary

    pokelist = [] #created a list 

    while low <= high:
        url = template.format(base=template, id=low)
        r = requests.get(url) #requests url from the internet, it gets the info from the url 
        if r.status_code is 200: #the status_code is 200 means that everything is GOOD AND PERFECT, now continue, if not stop
            the_json = json.loads(r.text) #r.text 
            tmp_dict["name"] = the_json["name"] #assigning stuff to our dictionary 
            tmp_dict["weight"] = the_json["weight"] #assigning stuff to our dictionary 
            tmp_dict["height"] = the_json["height"] #assigning stuff to our dictionary 
            pokelist.append(tmp_dict.copy()) # .copy() is really important otherwise we are adding references to the same dictionary over & over again
            low += 1 #increases low by 1 everytime the loop ocurs up until low > high

    index = 0 #Gets the index of the tallest pokemon
    tmp = 0 #Sets initial height compare to 0
    for x in range(len(pokelist)):
        if pokelist[x]["height"] > tmp:
            tmp = pokelist[x]["height"]
            index = x


    return {"name": pokelist[index]["name"], "height": pokelist[index]["height"],
            "weight": pokelist[index]["weight"]} #returns another dictionary 


def diarist():
    """Read gcode and find facts about it.
    Read in Trispokedovetiles(laser).gcode and count the number of times the
    laser is turned on and off. That's the command "M10 P1".
    Write the answer (a number) to a file called 'lasers.pew' in the week4 directory.
    TIP: you need to write a string, so you'll need to cast your number
    TIP: Trispokedovetiles(laser).gcode uses windows style line endings. CRLF
         not just LF like unix does now. If your comparison is failing this
         might be why. Try in rather than == and that might help.
    TIP: remember to commit 'lasers.pew' and push it to your repo, otherwise
         the test will have nothing to look at.
    TIP: this might come in handy if you need to hack a 3d print file in the future.
    """

    gcode = open(LOCAL + "/week4/Trispokedovetiles(laser).gcode", "r") #This opens the file
    on_off_count = 0 #This is the intial count
    for script in gcode:
        print(script) #Prints script
        if "M10 P1" in script:
            on_off_count += 1 #Everytime "M10 P1" is in the script the count increases by 1 
    f = open("lasers.pew", "w") #Opens lasers.pew file
    f.write(str(on_off_count)) #Writes 
    f.close #Closes
    pass



if __name__ == "__main__":
    functions = [
        obj
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if (inspect.isfunction(obj))
    ]
    for function in functions:
        try:
            print(function())
        except Exception as e:
            print(e)
    if not os.path.isfile("lasers.pew"):
        print("diarist did not create lasers.pew")



