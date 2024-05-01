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
# Chronotype: int : What's your Chronotype?
#                   0 = Night Owl
#                   1 = Morning Bird
#                   999 = Doesn't Matter
class account:
    def __init__(self, name, age, gender, grade, religion, drugs, neatness, chronotype):
        self.name = name
        self.age = age
        self.gender = gender
        self.grade = grade
        self.religion = religion
        self.drugs = drugs
        self.neatness = neatness
        self.chronotype = chronotype

# Critera is a slightly modified account with different fields to account for range values
# These values would be entered by a form questionaire with text-entry, dropdowns, and radio buttons.
class accountCriteria:
    def __init__(self, minAge, maxAge, gender, grade, religion, drugs, minNeatness, maxNeatness, chronotype):
        self.minAge = minAge
        self.maxAge = maxAge
        self.gender = gender
        self.grade = grade
        self.religion = religion
        self.drugs = drugs
        self.minNeatness = minNeatness
        self.maxNeatness = maxNeatness
        self.chronotype = chronotype

criteria = accountCriteria(18, 20, 0, 2, 999, 0, 3, 5, 0)
acc1 = account("John Doe", 19, 0, 2, 2, 0, 3, 1)
acc2 = account("Jane Doe", 18, 22, 0, 0, 2, 4, 1)
acc3 = account("Chris Topher", 22, 23, 3, 0, 1, 3, 0)

# This would be the actual accoutn database in the real thing
accDatabase = [acc1, acc2, acc3]
roommateList = []

def roommateFinder():
    # Return list for successful matches
    returnList = []
    
    for a in accDatabase:
        # Count of matches with criteria
        matchCount = 0

        # How old would you like your roommate
        if (criteria.minAge != 999 and criteria.maxAge != 999):
            if (a.age >= criteria.minAge and a.age <= criteria.maxAge):
                matchCount += 1

        # What is the preferred gender of your roommate?
        if (criteria.gender != 999):
            if (a.gender == criteria.gender):
                matchCount += 1
        
        # What is the preferred grade-level of your roommate?
        if (criteria.grade != 999):
            if (a.grade == criteria.grade):
                matchCount += 1

        # What is the preferred religion of your roommate?
        if (criteria.religion != 999):
            if (a.religion == criteria.religion):
                matchCount += 1

        # What is your stance on drug use?
        if (criteria.drugs != 999):
            if (a.drugs == criteria.drugs):
                matchCount += 1

        # How much does cleanliness matter to you?
        if (criteria.minNeatness != 999 and criteria.maxNeatness != 999):
            if (a.neatness >= criteria.minNeatness and a.neatness <= criteria.maxNeatness):
                matchCount += 1

        # What's your Chronotype? Are you an Early Bird or a Night Owl?
        if (criteria.chronotype != 999):
            if (a.chronotype == criteria.chronotype):
                matchCount += 1
        
        # Add the match count to the account object
        a.matchCount = matchCount
        
        # If student passes all checks, add them to the return list of successful matches
        if(matchCount > 0):
            returnList.append(a)

    # Sort the return list by match count in descending order
    returnList.sort(key=lambda x: x.matchCount, reverse=True)
    
    # If there are no perfect matches, return the sorted list
    return returnList

# Save list of returned roommates
roommateList = roommateFinder()

# Print Names of Matching Roommates
print("Successful Matches: ")
for r in roommateList:
    print(r.name, "- Number of Matches:", r.matchCount)