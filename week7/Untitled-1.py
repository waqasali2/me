#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'course/week7'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # Pandas
# 
# This notebook covers a _lot_, go through it carefully and _read_ the code. Then work on _understanding_ it. Then apply it to your data set. Then once you've done that, you'll probably _actually_ understand it.
# 
# Messing about with the [NSW Penalty data](http://www.osr.nsw.gov.au/sites/default/files/file_manager/penalty_data_set_0.csv)
#%% [markdown]
# `imports`, you've seen this before!

#%%
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

#%% [markdown]
# Some magic that tells jupyter to put graphs and things in the notebook instead of the default behaviour which is to save it as a file.

#%%
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (20, 10)


#%%
saved_style_state = matplotlib.rcParams.copy() #give us a style state to go back to

#%% [markdown]
# Let's check to see if we've already downloaded the data. It's a big file, so we don't want to do it every time we run the code. Even just loading from file takes a few seconds!
# 
# Pandas is pretty smart, it can get data from the internet just as easily as from the file system, it just takes a bit longer.
# 

#%%
if os.path.isfile("penalty_data_set_0.csv"):
    filepath = "penalty_data_set_0.csv"
    print("loading from file")
else:
    filepath = "http://www.osr.nsw.gov.au/sites/default/files/file_manager/penalty_data_set_0.csv"
    print("loading from the internet")

penalty_data = pd.read_csv(filepath)
print("done")


#%%
penalty_data.head()

#%% [markdown]
# `dataframe.head()` gives the top 5 rows, if it was `dataframe.head(3)` it would give the top 3 rows. 
#%% [markdown]
# We can also get the list of columns out of the data frame

#%%
penalty_data.columns

#%% [markdown]
# This is useful for you when you are documenting your dataset, you can make each column a heading, and then describe that column's characteristics.
#%% [markdown]
# You can't index a row directly, you need to use the iloc property.
# 
# This gives us the row as a _Series_.
# 
# ↓

#%%
row_one = penalty_data.iloc[1]
row_one

#%% [markdown]
# Series objects are _very_ similar to dictionaries. They have more properties though.

#%%
row_one["OFFENCE_DESC"]

#%% [markdown]
# Doing the same thing on a dataframe gives us the whole column

#%%
penalty_data["FACE_VALUE"]


#%%
penalty_data["FACE_VALUE"].plot()

#%% [markdown]
# If we do a simple `plot` on this column we get a pretty dense, but useless graph. It much better one would be a histogram.

#%%
penalty_data["FACE_VALUE"].hist()

#%% [markdown]
# The problem we have now is that almost _all_ fines are less than $2000, but there's a very long tail that fills up the right of the graph.
#%% [markdown]
# Let's exclude all the values above $3000, and see what it looks like.
# 
# We can do that with a nice feature of pandas, boolean indexing:

#%%
penalty_data["FACE_VALUE"][penalty_data["FACE_VALUE"] < 3000].hist()

#%% [markdown]
# That's pretty crazy/powerful, so let's see that happen a bit more clearly.
# 
# We'll make our own series and call it  `some_numbers`
# 
# Let's give it the values 0-99 

#%%
# Note the capital S, I have no idea why they did that!
# but if you get an `AttributeError: 'module' object has no attribute 'series'` error...
#                 v
some_numbers = pd.Series(range(100))
some_numbers.head()

#%% [markdown]
# We can use boolean indexing to get just the values that are less than 8

#%%
some_numbers[some_numbers < 8]

#%% [markdown]
# Or we can be fancy and get the numbers that are less than 4 _or_ more than 97:

#%%
some_numbers[(some_numbers < 4) | (some_numbers > 97)] #this needs the round brackets,
                                                       # not really sure why.

#%% [markdown]
# We can be _really fancy_ too!
# 
# This needs to resolve to a list of booleans that matches the list of inputs. It's filtering only for values that are True.
# 
# If we use a list comprehension then we can do almost anything we like!

#%%
pets = ["Dog", "Goat", "pig", "Sheep", "Cattle", "Zebu", "Cat", "Chicken", "Guinea pig",         "Donkey", "duck", "Water buffalo", "Western honey bee", "dromedary camel", "Horse", 
        "silkmoth", "pigeon", "goose", "Yak", "Bactrian camel", "Llama", "Alpaca", "guineafowl",         "Ferret", "muscovy duck", "Barbary dove", "Bali cattle", "Gayal", "turkey", "Goldfish", 
        "rabbit", "Koi", "canary", "Society finch", "Fancy mouse", "Siamese fighting fish",         "Fancy rat and Lab rat", "mink", "red fox", "hedgehog", "Guppy"]

pets_series = pd.Series(pets)
pattern_of_bools = ["o" in x for x in pets_series]
print(pattern_of_bools)

pets_series[pattern_of_bools]

#%% [markdown]
# _Note: the first `in` means a different thing to the second `in`. I was wondering if I should leave this out, but it's probably good to expose you to strange stuff!_
#%% [markdown]
# Anyway, back to our fines, it looks like we have a similar pattern of fines here, lots at the bottom end, not so many high value ones. 

#%%
penalty_data["FACE_VALUE"][penalty_data["FACE_VALUE"] < 3000].hist()

#%% [markdown]
# Let's see what's under $1000

#%%
penalty_data["FACE_VALUE"][penalty_data["FACE_VALUE"] < 1000].hist()

#%% [markdown]
# This warants some further investigation, but we'll come back to it in a bit. First, let's look at some of the other columns.
#%% [markdown]
# In the `LEGISLATION` column it tells us which law was invoked to give this fine. 

#%%
penalty_data["LEGISLATION"].value_counts()

#%% [markdown]
# *ROAD RULES 2008* and *2014* are pretty popular, but only one person got a ticket under the *COMBAT SPORTS REGULATION 2014* and one other person got booked for something under the *TATTOO PARLOURS REGULATION 2013*

#%%
penalty_data["LEGISLATION"].value_counts().plot(kind="bar")

#%% [markdown]
# We're going to see this distribution over and over again as we look at all kinds of data set.
# 
# These are probably the most common distributions, but they leave off the [power law](https://en.wikipedia.org/wiki/Power_law), which I think this probably is. 
# ![](http://blog.cloudera.com/wp-content/uploads/2015/12/distribution.png)
# [img](http://blog.cloudera.com/blog/2015/12/common-probability-distributions-the-data-scientists-crib-sheet/)

#%%
pdvc = penalty_data["LEGISLATION"].value_counts()
pdvc[pdvc < 5000].plot(kind="bar")

#%% [markdown]
# This pattern keeps repeating itself:

#%%
pdvc[pdvc < 1000].plot(kind="bar")


#%%
pdvc[pdvc < 100].plot(kind="bar")


#%%
pdvc[pdvc < 10].plot(kind="bar")

#%% [markdown]
# # Making plots nice
#%% [markdown]
# I said we'd come back to our histogram. [Here's a demo histogram from the matplotlib website](http://matplotlib.org/1.2.1/examples/pylab_examples/histogram_demo.html).

#%%
# This bit makes some random data. Ignore it
mu, sigma = 100, 15; x = mu + sigma*np.random.randn(10000)


#%%
# the histogram of the data
plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$') # allows for latex formatting
# plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()


#%%
# the histogram of the data
plt.hist(x, 50, density=True, facecolor='green', alpha=0.75)
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$') # allows for latex formatting
# plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()

#%% [markdown]
# Here's how we made our histogram before:

#%%
penalty_data["FACE_VALUE"][penalty_data["FACE_VALUE"] < 1000].hist()

#%% [markdown]
# And this is how we'd change it so that we can add more features:

#%%
capped_face_value_data = penalty_data["FACE_VALUE"][penalty_data["FACE_VALUE"] < 1000]

plt.hist(capped_face_value_data)
plt.show()

#%% [markdown]
# Let's look at some of the things we can do to this. The docs for histograms are here: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.hist

#%%
capped_face_value_data = penalty_data["FACE_VALUE"][penalty_data["FACE_VALUE"] < 1000]

plt.hist(capped_face_value_data, bins=10, facecolor='blue', alpha=0.2) #<-old one
plt.hist(capped_face_value_data, bins=50, facecolor='green', alpha=1)  #<-new one
plt.show()

#%% [markdown]
# We can go back to our initial, unfiltered, data:

#%%
plt.hist(penalty_data["FACE_VALUE"], bins=50)
plt.show()

#%% [markdown]
# Instead of doing the filtering before we present the data, we can use the graph to hide the extents of an axis:

#%%
plt.hist(penalty_data["FACE_VALUE"], bins=50, range=(0, 2000))
plt.show()

#%% [markdown]
# We can nice that up a bit by pulling the parameters out as variables:
# (unmagically, no difference!)

#%%
number_of_bins = 50
lower_bound = 0
upper_bound = 1000
plt.hist(penalty_data["FACE_VALUE"], bins=number_of_bins, range=(lower_bound, upper_bound))
plt.show()

#%% [markdown]
# This is still pretty naughty, we should have at least a title and some axis lables.
#%% [markdown]
# We do that by setting some more properties on the `plt` object:

#%%
number_of_bins = 100
lower_bound = 0
upper_bound = 1000

plt.hist(penalty_data["FACE_VALUE"], bins=number_of_bins, range=(lower_bound, upper_bound))
plt.title("Number of fines of a given value issued between {} and {}".format("then", "now"), fontsize=18)
plt.xlabel('$ value of fine', fontsize=26)
plt.ylabel('Count', fontsize=26)
plt.grid(True)
plt.show()

#%% [markdown]
# We could get the dates from the dataset if we wanted to be clever about it.
#%% [markdown]
# If we reimport the date, but with a bit more cleverness, we can tell pandas to convert the dates to actual dates.
# 
# Because _we_ are civilised, we use either iso dates `YYYY-MM-DD` or `DD-MM-YYYY`, but often you'll have to deal with data prepared by savages who don't respect this rational behaviour. They will use `MM-DD-YY` and other such primitive formats.
# 
# The settings used here control how it's read. You can only really tell by looking at the data and working it out. E.g. are there months bigger than 12?

#%%
penalty_data = pd.read_csv(filepath,
                           infer_datetime_format=True,
                           parse_dates=['OFFENCE_MONTH'],
                           dayfirst=True)
penalty_data.head(2)

#%% [markdown]
# This is some straight up, powerful voodoo.
# 
# We're grouping the fines by month, and then adding up the groups. Pandas' `groupby` feature allows for all kinds of clever stuff like that.

#%%
income = penalty_data[["OFFENCE_MONTH","FACE_VALUE"]].groupby("OFFENCE_MONTH").sum()

plt.xkcd()
plt.plot(income, "x-")
plt.title("Monthly income from fines", fontsize=18)
plt.xlabel('Date', fontsize=26)
plt.ylabel('$ Value', fontsize=26)
plt.grid(True)
plt.show()


#%%
matplotlib.rcParams.update(saved_style_state) # revert to regular matplotlib styles, not xkcd

#%% [markdown]
# I don't expect you to learn this this week, I just want to give you a taste of what can be done, quite simply, with pandas and matplotlib.
#%% [markdown]
# # some tricky tricks
#%% [markdown]
# Say you have a _lot_ of rows, running things on them takes a long time. You can test on a subset of that and then come bakc to the full dataframe once you are more sure that it works.
# 
# To do this we can use python slices in combination with the dataframe's `.loc` property.

#%%
ss = penalty_data.loc[:5]

#%% [markdown]
# Let's say you want to apply a function to each row in a dataframe, and save the result as a new column in the dataframe. This is where `apply` come in handy.

#%%
ss["day"] = ss.apply(lambda x: x.OFFENCE_MONTH.day, axis=1)
ss.head(1)

#%% [markdown]
# Above is equivalent to below, it's up to you to decide what is more readable.

#%%
def my_f(x):
    return x.day

ss["day"] = ss.apply(my_f, axis=1)
ss.head(1)

#%% [markdown]
# How do we tell the computer to treat _facade_ and _fašade_ the same? What about _University of new south wales_, _University of New South Wales_, _University of NSW_, _UNSW_, _New-south_?
#%% [markdown]
# ## The answer is _folding_
#%% [markdown]
# _(This is a "pattern")_

#%%
def fold(given):
    """Return canonical versions of inputs."""
    
    # Use canonical variables so that you can define once, use many times.
    UNSW_canonical = "uni of stairs"
    ben_name_cannonical = "Ben Doherty"

    # dictionary of input:output pairs
    folds = {
        "University of new south wales": UNSW_canonical,
        "University of New South Wales": UNSW_canonical,
        "University of NSW": UNSW_canonical,
        "UNSW": UNSW_canonical,
        "New-south": UNSW_canonical,
        "BDoh": ben_name_cannonical,
        "Benny": ben_name_cannonical,
        "Mr Dockerty": ben_name_cannonical,
        "Oi, Dickehead!": ben_name_cannonical
    }

#     return folds[given] # needs a defensive part, but ommited for clarity.
    default_value = given
    return folds.get(given, default_value)

print(fold("New-south"))
print(fold("BDoh"))

#%% [markdown]
# # _fin_

