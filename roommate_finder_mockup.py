# Roommate Finder Feature Psuedo-Code

# -- PROCESS --
# 1. User answers questions about their search criteria, this is saved in a criteria object
#       This criteria object is basically a slightly modified account that is not inside the database, but has it's attributes set by the user.
# 2. Criteria object and an array of Account Objects from the database is sent into the Roommate Finder Function
# 3. The roommate finder function iterates across the entire account database and compares them to the criteria using the accountCompare() function
# 4. In the function, the attributes of the criteria and an account input are compared.
#       These comparisons are BINARY, meaning an object either passes all it's checks or it doesn't.
#       If we want to a do a hybrid with relevance-based scoring with amount of interests two people share in common, that may be a bit more work, but it's possible.
# 5.  If an account passes all checks, accountCompare will return true
# 6.  If the result is true, add the account to the results array, if not, don't do anything.
# 7.  Once the entire database has been checked return the array of matching accounts.
#       This can probably display a similar way to how our forum posts are displayed.
# 8.  If the return array is empty or no accounts have been found, display a basic "No results" text string in the search result's place.

# -- ACCOUNT FIELDS --
# Using ints instead of string comparisons because that's faster and a lot less likely to be victim of a typo
# Assume 999 is code for "Don't Care / No Info"
# Name: String: Students's Name
# Age: int : Student's age in years (calculated from birthday?)
# Gender : int : Student's Gender,
#                0 = Male
#                1 = Famale
#                999 = Don't Care
# Grade : int : Student's College Grade Level
#               0 = Freshman
#               1 = Sophmore
#               2 = Junior
#               3 = Senior
#               999 = Don't Care
# Religion : int : Student's religion
#               0 = Agnostic
#               1 = Atheist
#               2 = Christian
#               3 = Jewish
#               4 = Muslim
#               5 = Buddhist
#               6 = Hinduist
#               999 = Don't Care
# Drugs : int : Are you okay with drugs?
#               0 = Yes
#               1 = No
#               999 = Don't Care
# Neatness : int : Neatness on a scale of 1 to 5
#               1 = messy
#               5 = clean-freak
#               999 = Don't Care
# Interests : String Array : 3 interests that the account has
# Chronotype: int : What's your Chronotype?
#                   0 = Night Owl
#                   1 = Morning Bird
#                   999 = Doesn't Matter
class account:
    def __init__(self, name, age, gender, grade, religion, drugs, neatness, interests, chronotype):
        self.name = name
        self.age = age
        self.gender = gender
        self.grade = grade
        self.religion = religion
        self.drugs = drugs
        self.neatness = neatness
        self.interests = interests
        self.chronotype = chronotype

# Critera is a slightly modified account with different fields to account for range values
# These values would be entered by a form questionaire with text-entry, dropdowns, and radio buttons.
class accountCriteria:
    def __init__(self, minAge, maxAge, gender, grade, religion, drugs, minNeatness, maxNeatness, interests, chronotype):
        self.minAge = minAge
        self.maxAge = maxAge
        self.gender = gender
        self.grade = grade
        self.religion = religion
        self.drugs = drugs
        self.minNeatness = minNeatness
        self.maxNeatness = maxNeatness
        self.interests = interests
        self.chronotype = chronotype

criteria = accountCriteria(18, 20, 0, 2, 999, 0, 3, 5, 0, "Gaming")
acc1 = account("John Doe", 19, 0, 2, 2, 0, 3, 0, ["Gaming", "Gardening", "Stargazing"])
acc2 = account("Jane Doe", 18, 1, 0, 0, 1, 5, 1, ["Art", "Reading", "Photography"])
acc3 = account("Chris Topher", 22, 0, 3, 0, 1, 2, 999["Gaming", "Marathon Running", "Writing"])

# This would be the actual accoutn database in the real thing
accDatabase = [acc1, acc2, acc3]
roommateList = []

def roommateFinder():
    # Return list for successful matches
    returnList = []
    # check variable determines if a match is successful in a binary fashion
    check = True
    
    for a in accDatabase:

        # Reset the value of the check variable
        check = True

        # How old would you like your roommate
        # If the user does not care about age, skip this iteration
        if (criteria.minAge != 999 and criteria.maxAge != 999):
            print("checking " + a.name +"'s age...")
            if (a.age >= criteria.minAge and a.age <= criteria.maxAge):
                print(a.name + " passed the age check!")
            else:
                print(a.name + " did not pass the age check.")
                check = False

        # What is the preferred gender of your roommate?
        # If the user does not care about gender, skip this check
        # If the account failed a previous check, skip this check
        if (criteria.gender != 999 and check != False):
            print("checking " + a.name +"'s gender...")
            if (a.gender == criteria.gender):
                print(a.name + " passed the gender check!")
            else:
                print(a.name + " did not pass the gender check.")
                check = False
        
        # What is the preferred grade-level of your roommate?
        # If the user does not care about grade-level, skip this check
        # If the account failed a previous check, skip this check
        if (criteria.grade != 999 and check != False):
            print("checking " + a.name +"'s grade-level...")
            if (a.grade == criteria.grade):
                print(a.name + " passed the grade check!")
            else:
                print(a.name + " did not pass the grade check.")
                check = False

        # What is the preferred religion of your roommate?
        # If the user does not care about religion, skip this check
        # If the account failed a previous check, skip this check
        if (criteria.religion != 999 and check != False):
            print("checking " + a.name +"'s religion...")
            if (a.religion == criteria.religion):
                print(a.name + " passed the religion check!")
            else:
                print(a.name + " did not pass the religion check.")
                check = False

        # What is your stance on drug use?
        # If the user does not care about drug use, skip this check
        # If the account failed a previous check, skip this check
        if (criteria.drugs != 999 and check != False):
            print("checking " + a.name +"'s drug stance...")
            if (a.drugs == criteria.drugs):
                print(a.name + " passed the drug test!")
            else:
                print(a.name + " did not pass the drug test.")
                check = False

        # How much does cleanliness matter to you?
        # If the user does not care about cleanliness, skip this iteration
        # If the account failed a previous check, skip this check
        if (criteria.minNeatness != 999 and criteria.maxNeatness != 999 and check != False):
            print("checking " + a.name +"'s neatness...")
            if (a.neatness >= criteria.minNeatness and a.neatness <= criteria.maxNeatness):
                print(a.name + " passed the cleanliness check!")
            else:
                print(a.name + " did not pass the cleanliness check.")
                check = False
        
        # What is an interest you like?
        # If the user does not care about sharing an interest, skip this check
        # If the account failed a previous check, skip this check
        # Let's just say the default interet value for criteria if nothing is entered is "N/A"
        # Checking for an empty array might make this check more complicated, we'll see how it turns out.
        if (criteria.interests != "N/A" and check != False):
            print("checking " + a.name +"'s interests...")
            # If we do Interest by scoring, have the interestScore increment by 1 for every interest in common
            #interestScore = 0
            # The binary option
            # If the user has an interest in common, they will be a successful match, if not and interestFlag is false, they get thrown away
            interestFlag = False
            # iterate through the account's list of interests and compares it to the criteria's interest
            # Criteria's interest could be an array intstead of a string, but that might make things a bit more complicated 
            for i in a.interests:
                if (i == criteria.interests):
                    print(a.name + " shares an interest with you!")
                    # If a matching interest is found, turn the interest flag "True"
                    interestFlag = True
            # This is the "binary choice" option
            # If the student has no interests in common, throw them away
            # If we change to an interest scoring option, this can be removed
            if (interestFlag != True):
                print(a.name + " shares no interests with you")
                check = False

        # What's your Chronotype? Are you an Early Bird or a Night Owl?
        # If the user does not care about sleep schedules, skip this check.
        # If the account failed a previous check, skip this check
        if (criteria.chronotype != 999 and check != False):
            print("checking " + a.name +"'s chronotype...")
            if (a.chronotype == criteria.chronotype):
                print(a.name + " passed the chronotype check!")
            else:
                print(a.name + " did not pass the chronotype check.")
                check = False
        
        # If student passes all checks, add them to the return list of successful matches
        if(check == True):
            returnList.append(a)
            #If we want to sort the students by "interest score", we'd probably have to do it in here
            # However, I can't figure a way to store interest score between iterations without it being attached to the account as an extra throwaway field

    # At the end of the loop, return a list of successful matches
    return returnList

# Save list of returned roommates
roommateList = roommateFinder()

#Print Names of Matching Roommates
print("Successful Matches: ")
for r in roommateList:
    print(r.name)
