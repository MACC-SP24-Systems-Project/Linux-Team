import requests
import json
import csv
import re

def make_request(size):
  #this is the URL that the request is sent to
  #this link contains the values for the terms and years. YearCode and TermCode appear at the end, we will need to access these values to handle when the semester changes.
  url = "https://my.macc.edu/ICS/webserviceproxy/exi/rest/studentregistration/pagedsectiondataforsearch?Id=57&IdNumber=-1&YearCode=2023&TermCode=SP"

  #the payload is what gets sent on the request. Some of the values are not necessary, I have removed them in the C version.
  payload = json.dumps({
    "pageState": {
      "enabled": True,
      "keywordFilter": "",
      "quickFilters": [],
      "sortColumn": "",
      "sortAscending": True,
      "currentPage": 0,
      "pageSize": size, #this variable can be changed to modify how much data is requested
      "showingAll": False,
      "selectedAll": False,
      "excludedFromSelection": [],
      "includedInSelection": [],
      "advancedFilters": [ #This contains any information that would normally be entered through the form.
        {
          "name": "courseCode",
          "value": ""
        },
        {
          "name": "courseCodeType",
          "value": "0"
        },
        {
          "name": "courseTitle",
          "value": "" 
        },
        {
          "name": "courseTitleType",
          "value": "0"
        },
        {
          "name": "requestNumber",
          "value": ""
        },
        {
          "name": "instructorIds",
          "value": ""
        },
        {
          "name": "departmentIds",
          "value": ""
        },
        {
          "name": "locationIds",
          "value": ""
        },
        {
          "name": "competencyIds",
          "value": ""
        },
        {
          "name": "beginsAfter",
          "value": ""
        },
        {
          "name": "beginsBefore",
          "value": ""
        },
        {
          "name": "instructionalMethods",
          "value": ""
        },
        {
          "name": "sectionStatus",
          "value": ""
        },
        {
          "name": "startCourseNumRange",
          "value": ""
        },
        {
          "name": "endCourseNumRange",
          "value": ""
        },
        {
          "name": "division",
          "value": ""
        },
        {
          "name": "place",
          "value": ""
        },
        {
          "name": "subterm",
          "value": ""
        },
        {
          "name": "meetsOnDays",
          "value": "0,0,0,0,0,0,0"
        }
      ],
      "totalRows": 15,
      "filteredRows": 845,
      "quickFilterCounts": None
    }
  }, 
  indent=4
  )
  headers = {
    'authority': 'my.macc.edu',
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': '',
    'origin': 'https://my.macc.edu',
    'referer': 'https://my.macc.edu/ICS/Course_Offerings.jnz?portlet=Course_Search&screen=StudentRegistrationPortlet_CourseSearchView&screenType=next',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
  }

  response = requests.request("POST", url, headers=headers, data=payload).json() #this is what sends the request and stores the json from it in the response variable.

  with open('data.json', 'w') as f: #writes the json to file
      json.dump(response, f, indent=4, sort_keys=True) #dump all the json in the response variable to a file. indent and sort_keys are used to add in newline characters and spaces so the file can be read more easily by programmers.
      print("Request Success")

################################

def clean_json_file(path): #this function removes the html from the json
   with open(path) as file:
    string_json = file.read()

    #these terms will be removed from the data
    prefixes_to_remove = ["Course Code", "Credits", "Faculty", "Schedule", "Seats open", "Status", "Title"] #originally, the data would look something like this: "credits": "Credits3.00" - but we don't want the extra word, so this loop removes the repeated words.
    for prefix in prefixes_to_remove:
      string_json = string_json.replace(prefix, "") #iterate through and remove anything from the prefix array

    remove = re.compile("<.*?>") #grabs html tags
    cleaned_data = re.sub(remove, "", string_json) #remove anything that was matched by the regex
    with open(path, 'w') as f: #write the json that has been cleaned up over the old json in the same file
      f.write(cleaned_data)
      print("JSON Cleaned")
    
################################

def write_to_csv(json_path, csv_path): #this function is used once the data has been cleaned and sorted
    with open(json_path) as json_file:
        data = json.load(json_file)

    classes = data["rows"] #this grabs the rows key from the JSON file which contains all the classes, each class being one row

    data_file = open(csv_path, "w", newline="") #this creates/opens a file to write the csv to using the csv_path variable as the file

    csv_writer = csv.writer(data_file) #creating a csv writer in the file

    # Counter variable used for writing
    # headers to the CSV file
    count = 0
    for course in classes:
        if count == 0:
            #csv files have the names of the columns at the top of the file. This writes the headers to the top if we are on the first row. The headers are the keys used in the JSON file.

            # Writing headers of CSV file
            header = course.keys()
            csv_writer.writerow(header)
            count += 1 #this makes it so we don't write the header more than once.

        # Writing data of CSV file
        csv_writer.writerow(course.values()) #this writes every key and value that would appear in one row in the JSON file.

    data_file.close()

    print("CSV file written")

################################
    
#this function takes in a pattern, finds it, subracts it from the original and then returns both
def regex_finder(pattern, string): #the first parameter is the regex pattern to look for, the string is the text we want to match.
    sub_string = re.search(pattern, string) #make the match and assign it to the variable
    return(string.replace(sub_string.group(0), "").strip(), sub_string) #in the string.replace function call, the matched regex is removed from the original string and the shortened string is returned, then return the substring variable.
    #You can return more than one thing in Python, the multiple values are assigned in the order they are returned.

################################

def regex_extractor(data_string):
    #The uncleaned strings look like this: Tue9:00-10:20 AM1/17/2024 - 5/9/2024 MACC Columbia MACC-Columbia - 129   But if it was an online class or an internship or some other form of class, there are a few different things it could say.
    #The code checks to see if the string starts with a weekday by testing if the first 3 characters match anything in the weekdays array. In the example string above, the first 3 characters are "Tue", so it would then clean of the string.
    #but if it did not match then all the values normally used to store the scheduling data are set to N/A because that information does not exist.
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for d in weekdays:
        if  data_string.startswith(d):

            #the next lines are responsible for getting the data we want to store out of the string. It uses the function above this one.
            data_string, day = regex_finder(r'^\b[A-Za-z]{3}(?:,\s?[A-Za-z]{3})?', data_string)
            #assuming the example string was used here:
            #now data_string = 9:00-10:20 AM1/17/2024 - 5/9/2024 MACC Columbia MACC-Columbia - 129
            #and day = Tue

            data_string, time = regex_finder(r'^\b[0-9]{1,2}:[0-9]{2}\s?(?:[A|P]M)?-[0-9]{1,2}:[0-9]{2}\s?[A|P]M', data_string)
            #now data_string = 1/17/2024 - 5/9/2024 MACC Columbia MACC-Columbia - 129
            #and time = 9:00-10:20 AM

            data_string, date = regex_finder(r'^[\d]{1,2}/[\d]{1,2}/[\d]{4}\s?-\s?[\d]{1,2}/[\d]{1,2}/[\d]{4}', data_string) #same thing for the next 2 function calls

            data_string, campus = regex_finder(r'^[\w]+\s[\w]+', data_string)

            room = data_string #room is the last bit left over, but because everything else has been removed by now there is no reason to continue using regex

            new_info = { #this is the JSON variable that stores all of the data we just gathered.
                "day": day.group(0),
                "time": time.group(0),
                "date": date.group(0),
                "campus": campus.group(0),
                "room": room
            }

            return new_info #because the data has been collected, we need to escape the loop to avoid overwriting it 
        else:
            #if we are in this else statement, it's because the string did not start with a day of the week. This is because it's either an online class, or some other form of class with no official meeting time and place.
            #for this just assign everything to N/A and return it, there is no data to store.
            day = time = room = date = campus = "N/A"

            new_info = { #construct a new piece of json and return it
                "day": day,
                "time": time,
                "date": date,
                "campus": campus,
                "room": room
            }

    return new_info

################################

def seperate_scheduling_data(file_path): #this function just calls the schedule cleaning function for every value under the key "row" in the JSON file.
    with open(file_path) as json_file:
        data = json.load(json_file)

    for row in data["rows"]: #remember that every row is a class, so every row needs to be cleaned.
        row.update(regex_extractor(row["schedule"])) #this calls the function to clean up the data and it adds in the returned JSON to the row
        row.pop("schedule") #this removes the old string that is not wanted anymore
    
    with open(file_path, 'w') as f: #write the adjusted json
      json.dump(data, f, indent=4, sort_keys=True) #this just writes the improved JSON back over the old JSON
      print("Scheduling data cleaned")

################################

if __name__ == "__main__": #this calls all of the functions in the if statement if the script is the main script. This prevents the functions being called if this script was included in another script. Similar to int main() in C++
  make_request(15)
  clean_json_file("data.json")
  seperate_scheduling_data("data.json")
  write_to_csv("data.json", "data.csv")