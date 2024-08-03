import re

def parse_personal_info(text):

    personal_info_pattern = r"İsim: (.*?), Doğum Tarihi: (.*?),"
    personal_info_match = re.search(personal_info_pattern, text)
    if personal_info_match:
        name = personal_info_match.group(1)
        birth_date = personal_info_match.group(2)

def parse_education_history(text):
    education_pattern = r"(\d{4})-(\d{4}): (.*?), (.*?), (.*?),"
    education_matches = re.findall(education_pattern, text)
    for match in education_matches:
        start_year = match[0]
        end_year = match[1]
        degree = match[2]
        field_of_study = match[3]
        institution = match[4]

def parse_experience(text):
    experience_pattern = r"(\d{4})-(\d{4}): (.*?), (.*?),"
    experience_matches = re.findall(experience_pattern, text)
    for match in experience_matches:
        start_year = match[0]
        end_year = match[1]
        title = match[2]
        company = match[3]

def parse_skills(text):

    skills_pattern = r"Yazılım Dilleri: (.*?),"
    skills_match = re.search(skills_pattern, text)
    if skills_match:
        skills = skills_match.group(1).split(', ')

with open("cv.txt", "r", encoding="utf-8") as file:
    cv_text = file.read()

parse_personal_info(cv_text)
parse_education_history(cv_text)
parse_experience(cv_text)
parse_skills(cv_text)
