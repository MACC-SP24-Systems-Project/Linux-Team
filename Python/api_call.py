import requests
import json
import csv
import re

def make_request(size):
  url = "https://my.macc.edu/ICS/webserviceproxy/exi/rest/studentregistration/pagedsectiondataforsearch?Id=57&IdNumber=-1&YearCode=2023&TermCode=SP"

  payload = json.dumps({
    "pageState": {
      "enabled": True,
      "keywordFilter": "",
      "quickFilters": [],
      "sortColumn": "",
      "sortAscending": True,
      "currentPage": 0,
      "pageSize": size,
      "showingAll": False,
      "selectedAll": False,
      "excludedFromSelection": [],
      "includedInSelection": [],
      "advancedFilters": [
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

  response = requests.request("POST", url, headers=headers, data=payload).json()

  with open('data.json', 'w') as f: #writes the dirty json to the file
      json.dump(response, f, indent=4, sort_keys=True)
      print("Request Success")

################################

def clean_json_file(path): #this function removes the html from the json
   with open(path) as file:
    string_json = file.read()
    remove = re.compile("<.*?>") #regex that grabs html tags

    #these terms will be removed from the data
    prefixes_to_remove = ["Course Code", "Credits", "Faculty", "Schedule", "Seats open", "Status", "Title"]
    for prefix in prefixes_to_remove:
      string_json = string_json.replace(prefix, "") #iterate through and remove anything from the prefix array

    cleaned_data = re.sub(remove, "", string_json)
    with open(path, 'w') as f: #write the json that has been cleaned up over the old json in the same file
      f.write(cleaned_data)
      print("JSON Cleaned")
    
################################

def write_to_csv(json_path, csv_path):
    with open(json_path) as json_file:
        data = json.load(json_file)

    classes = data["rows"]

    data_file = open(csv_path, "w", newline="")

    csv_writer = csv.writer(data_file)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0
    for course in classes:
        if count == 0:

            # Writing headers of CSV file
            header = course.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(course.values())

    data_file.close()

    print("CSV file written")

################################
    
#this function takes in a pattern, finds it, subracts it from the original and then returns both
def regex_finder(pattern, string):
    sub_string = re.search(pattern, string)
    return(string.replace(sub_string.group(0), "").strip(), sub_string)

################################

def regex_extractor(data_string):
    #this array is used to test if the first word is a weekday, if not then its an online class and this data can be ignored
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for d in weekdays:
        if  data_string.startswith(d):

            #go through and grab the data, subtract it from the data, store both. Now we have all our data in pieces
            data_string, day = regex_finder(r'^\b[A-Za-z]{3}(?:,\s?[A-Za-z]{3})?', data_string)

            data_string, time = regex_finder(r'^\b[0-9]{1,2}:[0-9]{2}\s?(?:[A|P]M)?-[0-9]{1,2}:[0-9]{2}\s?[A|P]M', data_string)

            data_string, date = regex_finder(r'^[\d]{1,2}/[\d]{1,2}/[\d]{4}\s?-\s?[\d]{1,2}/[\d]{1,2}/[\d]{4}', data_string)

            data_string, campus = regex_finder(r'^[\w]+\s[\w]+', data_string)

            #because the room information is all that is left when we get here, there is no reason to use regex
            room = data_string

            new_info = { #construct a new piece of json and return it
                "day": day.group(0),
                "time": time.group(0),
                "date": date.group(0),
                "campus": campus.group(0),
                "room": room
            }

            return new_info #because the data has been collected, we need to escape the loop to avoid overwriting it 
        else:
            day = time = date = campus = "N/A"
            room = "Virtual"

    new_info = { #construct a new piece of json and return it
                "day": day,
                "time": time,
                "date": date,
                "campus": campus,
                "room": room
            }

    return new_info

def seperate_scheduling_data(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)

    for row in data["rows"]: #go through and add in the seperated data
        row.update(regex_extractor(row["schedule"]))
        row.pop("schedule") #remove the old data that is messy
    
    with open(file_path, 'w') as f: #write the adjusted json
      json.dump(data, f, indent=4, sort_keys=True)
      print("Scheduling data cleaned")

################################

if __name__ == "__main__":
  make_request(15)
  clean_json_file("data.json")
  seperate_scheduling_data("data.json")
  write_to_csv("data.json", "data.csv")