# :: 1st FEB 2020 || SAHIL SARNA ::

# This program scraps the data of 10 random actors (plus Leonardo DiCaprio) from IMDB's Website
# Gets the Name, Rank and Date of Birth and Birthplace of the actor
# Display's a neat table in the console of all the scrapped data
# At the end exports the data into an excel file

import requests
from random import randint
from bs4 import BeautifulSoup
import pandas as pd

# https://www.imdb.com/name/nm0000138/
urlTemplate = "https://www.imdb.com/name/nm{}/"

# Empty urlList to add URLs to
urlList = []

# Will give the addresses for 10 RANDOM Actors
for x in range(1, 11):
    y = str(randint(1, 1000))
    urlList.append(urlTemplate.format(y.zfill(7)))

# Print out all the URLs
# print(urlList)

# Add a known actor address to check values (Leonardo DiCaprio)
urlList.append("https://www.imdb.com/name/nm0000138/")

# Empty Actor's List to add actors data to
actorRecord = []

# Iterate through all URLs
for url in urlList:

    # Which URL the data is coming from
    print(url)
    resp = requests.get(url)
    # Check the response code
    print("RESPONSE CODE: ", resp.status_code)
    # Proceed if code is 200 (Good Status)
    if resp.status_code == 200:
        # Get Page Data
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Actor's Name
        actorName = soup.find('span', {'class':'itemprop'}).text
        print(actorName)

        # Actor's Rank
        if soup.find('a', {'id':'meterRank'}).text == "SEE RANK":
            meterRank = "Above Top 5000"
        else:
            meterRank = soup.find('a', {'id':'meterRank'}).text
        print(meterRank)

        # Actor's Date of Birth
        dob = soup.find('div', {'id':'name-born-info'}).text.replace("  "," ").replace("\n", "").replace("Born:","")
        dob = " ".join(dob.split())
        # dob = soup.find('time').text.replace("\n","").replace("   "," ").replace("  "," ")
        print(dob)

        # Make a list of actors record
        actorRecord.append((actorName, meterRank, dob))

# print(actorRecord)

# :: PRINT TABLE ::

# Table Heading
print("\n{}".format("ACTORS LIST".center(85, " ")))
# Count for Serial Numbers
count = 1
# Field Headings
print (("{} {} {} {}").format("SN ", "NAME".ljust(30, " "), "RANK".ljust(15, " "), "BIRTH".ljust(50, " ")))
# Print Data
for x in actorRecord:
    print(("{}) {} {} {}").format(str(count).zfill(2), x[0].ljust(30, " "), x[1].ljust(15, " "), x[2].ljust(50, " ")))
    # Increment Count for next
    count += 1


# :: EXPORT DATA ::

# Put all the actors data into a data frame (Need to import pandas)
df = pd.DataFrame(
    {
        "NAME" : [ x[0] for x in actorRecord ],
        "RANK" : [ x[1] for x in actorRecord ],
        "BIRTH": [ x[2] for x in actorRecord ]
    }
)

# Exports the data to an excel file (Need to have a module openpyxl)
df.to_excel("IMDBActorsRatings.xlsx")