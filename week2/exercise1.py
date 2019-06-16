"""
Commenting skills:

TODO: above every line of code comment what you THINK the line below does.
TODO: execute that line and write what actually happened next to it.

See example for first print statement
"""
import platform

# I think this will print "hello! Let's get started" by calling the print function.
print("hello! Let's get started")  # it printed "hello! Let's get started"

some_words = ['what', 'does', 'this', 'line', 'do', '?']

#over here "word" is a temporary variable. It will print all the words in the some_words function 
for word in some_words:
    print(word) #prints all words present in some_words

#This is the same as above, but the temporary variable has been named x
for x in some_words:
    print(x) #prints all words presesnt in some_words :)

print(some_words) #prints all words present in some_words

#This is a if statement, if the statement is true i think it will print "some_words contains more than 3 words"
if len(some_words) > 3:
    print('some_words contains more than 3 words') #printed "some_words contains more than 3 words"

#This defines a function
def usefulFunction():
    """
    You may want to look up what uname does before you guess
    what the line below does:
    https://docs.python.org/3/library/platform.html#platform.uname
    """
    print(platform.uname()) #prints the platform name that the user is using, e.g Mac 

usefulFunction()
