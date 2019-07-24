TODO: Reflect on what you learned this week and what is still unclear.

Lecture 5 Notes
- Big indentation is a no no 

Notes 
#lets create a url that can be changed as we loop again and again
URL = "http://api.wordnik.com/v4/words.json/randomWords?api_key={api_key}&minLength={length}&maxLength={length}&limit=1" 
#in areas where we want to alter detail of teh link we use {} as a place holder 

#here we create the format
url = URL.format(api_key = "owpgbi1ig2erl892n1c02dgw2y31hgtxnb4xub3qqq133jhn6", length = length)
#you can see that we use URL.format, which means we are formating the url. her we assign values to the place holder 

#requesting a url
r = requests.get(url)
#to request a url we use requests.get(x)

#
r.status_code is 200:
#this makes sure that shit is all good and is working perfectly 

we learned how to label a triangle, notes for those are on the exercises 

