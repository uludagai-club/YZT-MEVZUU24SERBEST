import json

cv_text = {
    "Education": "Stanford University",
    "GPA": 3.78,
    "Certificy": "Certificate of Approval",
    "Soft Skill": "Leadership",
    "Hard Skill": "Python programming",
    "Language": "English",
    "Work Experience": "Software Engineer at XYZ Company",
    "Hobby": "Music",
    "Reference": "John Doe",
    "Expert": "Data Science",
    "Abstract": "Summary",
    "Voluntary": "Volunteer at ABC Organization",
    "Contact": "john.doe@example.com",
    "Driver License": "Yes",
    "Country": "USA"
}

def gpa_account(GPA):
    if GPA >= 3.5:
        return "Very Good"
    elif GPA >= 3.0:
        return "Good"
    elif GPA >= 2.5:
        return "Medium Good"
    else:
        return "Bad"

doc_name = "university_multiple.json"
with open(doc_name, 'r') as document:
    university_multipliers = json.load(document)

def score_account(Education, GPA):
    for item in university_multipliers:
        if item["University"] == Education:
            global_rank = item["Global Rank"]
            global_score = item["Global Score"]
            state = item["State"]
            national_rank = item["National Rank"]
            national_score = item["National Score"]
            score = global_score * GPA
            score1 = national_score * GPA
            return (global_rank, global_score, state, national_rank, national_score, score, score1)
    return None, None, None, None, None, None, None

Education = cv_text.get("Education")
GPA = cv_text.get("GPA")
preferred_state = input("Enter state:")

if Education and GPA:
    gpa_value = gpa_account(GPA)
    global_rank, global_score, state, national_rank, national_score, score, score1 = score_account(Education, GPA)
    if global_rank is not None:
        print("University:", Education)
        print("GPA:", GPA)
        print("GPA Value:", gpa_value)
        print("Global Rank:", global_rank)
        print("Global Score:", global_score)
        print("State:", state)
        if state == preferred_state:
          print("National Rank:", national_rank)
          print("National Score:", national_score)
          print("Score1:", score1)
        print("Score:", score)
    else:
        print("University not found in data.")
else:
    print("University or GPA not found.")