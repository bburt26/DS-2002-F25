import csv
with open("raw_survey_data.csv", "w", newline = "") as f:
    writer = csv.writer(f)
    writer.writerow(["student_id", "major", "GPA", "is_cs_major", "credits_taken"])
    writer.writerow([101, "spanish", 4, 'No', '15.0'])
    writer.writerow([102, "computer science", 3, 'Yes', '17.0'])
    writer.writerow([103, "english", 3.7, 'No', '12.0'])
    writer.writerow([104, "biology", 3.2, 'No', '15.0'])
    writer.writerow([105, "chemistry", 4, 'No', '18.0'])


import json

classes = [
  {
    "course_id": "DS2002",
    "section": "001",
    "title": "Data Science Systems",
    "level": 200,
    "instructors": [
      {"name": "Austin Rivera", "role": "Primary"}, 
      {"name": "Heywood Williams-Tracy", "role": "TA"} 
    ]
  },
  {
    "course_id": "SPAN4520",
    "title": "Culture and Civilization",
    "level": 400,
    "instructors": [
      {"name": "Fernando Riva", "role": "Primary"}
    ]
  },
]
with open("raw_course_catalogue.json", "w") as f:
    json.dump(classes, f, indent = 4)


import pandas as pd
survey = pd.read_csv("raw_survey_data.csv")
print(survey)

def enforce_boolean(entry):
    if entry == "Yes":
      return True
    elif entry == "No":
        return False
survey["is_cs_major"] = survey["is_cs_major"].apply(enforce_boolean)
print(survey)

survey["GPA"] = survey["GPA"].astype(float)
survey["credits_taken"] = survey["credits_taken"].astype(float)
print(survey["GPA"].dtypes)
print(survey["credits_taken"].dtypes)

survey.to_csv("clean_survey_data.csv", index = True)

import json
with open("raw_course_catalogue.json", 'r') as file:
   classes = json.load(file)

normalize = pd.json_normalize(classes, record_path=['instructors'], meta=['course_id', 'title', 'level'])
print(normalize)
normalize.to_csv("clean_course_catalogue.csv", index = True)

print("clean_survey_data.csv")

print("clean_course_catalogue.csv")
