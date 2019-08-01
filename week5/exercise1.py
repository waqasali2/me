# -*- coding: UTF-8 -*-
"""Refactoring.

This exercise contains a complete and working example, but it's very poorly written.

Your job is to go through it and make it as good as you can.

That means making it self-documenting wherever possible, adding comments where
it isn't. Take repeated code and make it into a function. Also use functions
to encapsulate concepts. If something is done many times, maybe a map or a loop
is called for. Etc.

Some functions will have directions as external comments, once you think you
are on top of it, take these comments out. Others won't have comments and
you'll need to figure out for yourself what to do.
"""

# return a list of countdown messages, much like in the bad function above.
# It should say something different in the last message.
def countdown(message, start, stop, completion_message):
    """for count in reversed(range(stop-stop +1,start-stop+2)): #counts in reverse 
        print(message + " " + str(count)) #prints the message + a space for the words + the numbers (in string format)
    print(completion_message) #prints completion_message
    """
    countdown = [] #created a list 
    for j in range(start-stop+1, stop-stop, -1): # we have this range of numbers that we want 
        print(message,str(j)) #prints the string and message 
    print(completion_message) #prints completion message 
    return countdown #returns it 
    
# TRIANGLES
# This should be a series of functions that are ultimatly used by
# triangle_master
# It should eventually return a dictionary of triangle facts. It should
# optionally print information as a nicely formatted string. Make printing
# turned off by default but turned on with an optional argument.
# The stub functions are made for you, and each one is tested, so this should
# hand hold quite nicely.
def calculate_hypotenuse(base, height):
    import math
    hypotenuse = math.sqrt(base ** 2 + height ** 2)
    return hypotenuse #the return command ends the thingo as well as prints the function


def calculate_area(base, height):
    import math
    area = 0.5*(base * height)
    return area


def calculate_perimeter(base, height):
    import math
    perimeter = base + height + calculate_hypotenuse(base, height)
    return perimeter


def calculate_aspect(base, height):
    if base > height:
        aspect = "wide"
    elif base == height:
        aspect = "equal"
    else:
        aspect = "tall"    
    return aspect



# Make sure you reuse the functions you've already got
# Don't reinvent the wheel
def get_triangle_facts(base, height, units="mm"):
    area_calc = calculate_area(base, height)
    aspect_cal = calculate_aspect(base, height)
    hypotenuse_calc = calculate_hypotenuse(base, height)
    perimeter_calc = calculate_perimeter(base, height)
    return {
        "area": area_calc,
        "perimeter": perimeter_calc,
        "height": height,
        "base": base,
        "hypotenuse": hypotenuse_calc,
        "aspect": aspect_cal,
        "units": units,
    }


# this should return a multi line string that looks a bit like this:
#
# 15
# |
# |     |\
# |____>| \  17.0
#       |  \
#       |   \
#       ------
#       8
# This triangle is 60.0mm²
# It has a perimeter of 40.0mm
# This is a tall triangle.
#
# but with the values and shape that relate to the specific
# triangle we care about.
def tell_me_about_this_right_triangle(facts_dictionary):
    tall = """
            {height}
            |
            |     |\\
            |____>| \\  {hypotenuse}
                  |  \\
                  |   \\
                  ------
                  {base}"""
    wide = """
            {hypotenuse}
             ↓         ∕ |
                   ∕     | <-{height}
               ∕         |
            ∕------------|
              {base}"""
    equal = """
            {height}
            |
            |     |⋱
            |____>|  ⋱ <-{hypotenuse}
                  |____⋱
                  {base}"""

    pattern = (
        "This triangle is {area}{units}²\n"
        "It has a perimeter of {perimeter}{units}\n"
        "This is a {aspect} triangle.\n"
    )

    facts = pattern.format(**facts_dictionary)

    if facts_dictionary["aspect"] == "wide":
        diagram = wide.format(**facts_dictionary)
    elif facts_dictionary["aspect"] == "tall":
        diagram = tall.format(**facts_dictionary)
    else:
        diagram = equal.format(**facts_dictionary)
    facts = pattern.format(**facts_dictionary)

    return(diagram + "\n" + facts)



def triangle_master(base, height, return_diagram=False, return_dictionary=False):
    fact1 = get_triangle_facts(base, height)
    info1 = tell_me_about_this_right_triangle(fact1)
    if return_diagram and return_dictionary:
        return {"diagram": info1, "facts": fact1}
    elif return_diagram:
        return info1
    elif return_dictionary:
        return fact1
    else:
        print("You're an odd one, you don't want anything!")


def wordy_pyramid(api_key):
    import requests

    URL = "http://api.wordnik.com/v4/words.json/randomWords?api_key={api_key}&minLength={length}&maxLength={length}&limit=1"
    pyramid_list = []
    for i in range(3, 21, 2):
        url = URL.format(api_key = "", length=i)
        r = requests.get(url)
        if r.status_code is 200:
            message = r.json()[0]["word"]
            pyramid_list.append(message)
        else:
            print("failed a request", r.status_code, i)
    for i in range(20, 3, -2):
        url = URL.format(api_key = "", length=i)
        r = requests.get(url)
        if r.status_code is 200:
            message = r.json()[0]["word"]
            pyramid_list.append(message)
        else:
            print("failed a request", r.status_code, i)
    return pyramid_list


def get_a_word_of_length_n(length):
    import requests
    URL = "https://us-central1-waldenpondpress.cloudfunctions.net/give_me_a_word?wordlength={len1}" #using the new link given,we are formating it such that we can change the length of the word that it gives back 
    if type(length) == int and length >= 3: #if the length is of type, integer, and is of length greater than or equal to 3 
        url=URL.format(len1=length) #format the link such that the it opens up to a word of length 'length'
        pull = requests.get(url) #this gets the formatted url 
        if pull.status_code is 200: #if shit is good        
            word_n = pull.content  #pulls in the content
            word_n = str(word_n) #ensures the word is a string
            output = word_n[2:len(word_n)-1] #we now have the word
        return output #returns the word 
    else:
        pass # essenttially restarts the cycle 


def list_of_words_with_lengths(list_of_lengths):
    """import requests
    URL = "http://api.wordnik.com/v4/words.json/randomWords?api_key=owpgbi1ig2erl892n1c02dgw2y31hgtxnb4xub3qqq133jhn6&minLength={length}&maxLength={length}&limit=1" #here we have the link that needs to be formatted 
    list =[] # we now have an empty list 
    for i in range(len(list_of_lengths)): #providing a range 
        length=list_of_lengths[i] #giving a length 
        url = URL.format(length=length) #url is now formatted 
        r = requests.get(url) #gets the formatted url 
        if r.status_code is 200: #if shit is good 
            words = r.json()[0]["word"] #grabs word
            list.append(words) #ads word to the list 
    return(list) #returns the list 
    """
    import requests
    list_length_x = [] #created a list 
    URL = "https://us-central1-waldenpondpress.cloudfunctions.net/give_me_a_word?wordlength={lengthx}" #our new formatable url
    for j in list_of_lengths:
        url = URL.format(lengthx=j) #url is now formatted 
        r = requests.get(url) #gets the url info 
        if r.status_code is 200: #if shit is good
            word = str(r.content) #a string
            return_x = word[2:len(word)-1] #returns word
        list_length_x.append(return_x) #puts word in list 
    return list_length_x

if __name__ == "__main__":
    do_bunch_of_bad_things()
    wordy_pyramid("a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5")
