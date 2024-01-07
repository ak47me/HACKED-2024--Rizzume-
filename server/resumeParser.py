import json
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import re
from pdfminer.high_level import extract_text

API_KEY = ''
openai = OpenAI(api_key=API_KEY)

def textgeneration(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}],
            temperature = 0.2
        
            )

    return response.choices[0].message.content

# getting text from job posting and classifying with GPT
def scrape_text_jobposting(url):
    try:
        # Send an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text content
            text_content = soup.get_text()
            # print("Text from soup: ",text_content)

            prompt = f'You are given this job description {text_content}, give me a json file with the following parameters only: requirements, skills, job description, responsibilities, programming languages .'

            content = textgeneration(prompt)
            # print("GPT simplified: ",content)
            #print(content)
            return content

        else:
            # print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None

    except Exception as e:
        # print(f"An error occurred: {e}")
        return None


def extract_resume(resume_location):
    resume_dict = {"GenDet":[],"Education":[],"Experience":[],"Projects":[],"TechSkills":[]}
    text = extract_text(resume_location)

    prompt_gen = f"Here is a resume: {text}.Extract the general details like name and links"
    content_gen = textgeneration(prompt_gen)
    resume_dict["GenDet"].append(content_gen)


    prompt_ed = f"Here is a resume: {text}.Extract the education part only"
    content_ed = textgeneration(prompt_ed)
    resume_dict["Education"].append(content_ed)

    prompt_exp = f"Here is a resume: {text}.Extract the Experience part only if exists"
    if prompt_exp:
        content_exp = textgeneration(prompt_exp)
        resume_dict["Experience"].append(content_exp)
    
    prompt_pro = f"Here is a resume: {text}.Extract the Projects part only"
    if prompt_pro:
        content_pro = textgeneration(prompt_pro)
        resume_dict["Projects"].append(content_pro)

    prompt_tech = f"Here is a resume: {text}.Extract the Technical skills part only"
    if prompt_tech:
        content_tech = textgeneration(prompt_tech)
        resume_dict["TechSkills"].append(content_tech)
    
    return resume_dict


def extract_jobdescription(jobposting):
    extrated_posting = {"requirements":[], "skills":[], "job description":[],"responsibilities":[],"programming languages":[]}
    # prompt = f"I have {extrated_posting} dictionary and {jobposting}.Parse the job description and return the given dictionary with the paramters filled in completely(not partially) "
    # result = textgeneration(prompt)
    # if result:
    #     data_dict = json.loads(result)
    # print(data_dict,type(data_dict))
    extrated_posting["requirements"] = textgeneration(f'Give me only the requirements of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the requirements')
    extrated_posting["skills"] = textgeneration(f'Give me only the skills of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the skills')
    extrated_posting["job description"] = textgeneration(f'Give me only the job description of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the job description')
    extrated_posting["responsibilities"] = textgeneration(f'Give me only the responsibilities of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the job description')
    extrated_posting["programming languages"] = textgeneration(f'Give me only the programming languages of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the programming languages')
    return extrated_posting

def pre_process():
        res = []
        file_path = 'resume_format.txt'

        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.readlines()

        # Initialize a variable to store the content before the marker
        content_before_marker = ""

        # Iterate through the lines to find the marker and capture the content above it
        for line in file_content:
            if "section ends here" in line:
                res.append(content_before_marker)
                content_before_marker = ""
            else:
                content_before_marker += line
        return res

# reading all files
def generate_resume(resume,jobposting,extracted_resume):
    result = ""
    
    def gen_general_details():
        gen_desc = extracted_resume["GenDet"]
        print(gen_desc)
        prompt_gen = f"i have general details from my resume {gen_desc}.Fill up just that part for this part:\n {resume[0]}"
        content_gen = textgeneration(prompt_gen)
        return content_gen
    def gen_edc():
        gen_edu = extracted_resume["Education"]
        prompt_edu = f"i have education details from my resume {gen_edu} .Fill up just that part for this part:\n {resume[1]}"
        content_edu = textgeneration(prompt_edu)
        return content_edu
    def gen_exp():
        # displays experience if exists
        gen_exp = extracted_resume["Experience"] + extracted_resume["Projects"]
        # prompt_exp = f"i have Experience details from my resume {gen_exp} .Fill up just that part for this part:\n {resume[2]}"
        prompt_exp = f'Here are my experiences from my resume that i made: {gen_exp} and here are the job description: {jobposting["job description"]} and skills: {jobposting["skills"]} such that it matches the top matching experiences and projects from my given resume that match all details of the job and  make it match it in this given format: {resume[2]}'
        content_exp = textgeneration(prompt_exp)
        return content_exp
    def gen_tech_skills():
        gen_skills = extracted_resume["TechSkills"]

        prompt_skills = f'Here are my skills that i know: {gen_skills} and here are the required skills for the job: {jobposting["skills"]} list the common skills and if the common skills are less than 3 then put important skills from the resume and do not put any extra preceding or trailing words and make it fit this format: {resume[-1]}'

        content_skills = textgeneration(prompt_skills)
        return content_skills

    a = gen_general_details()
    d = gen_edc()
    b = gen_exp()
    c = gen_tech_skills()
    
    result = a+d+b+c
    return result
    
def conver_to_latex(resume):
    with open("resume_format.txt", 'r') as file:
        resumeformat = file.read()
    prompt = f'Convert this resume {resume} into latex using the following template {resumeformat} make sure to put everything from the resume I provided.I dont want any preceding or trailing words!.Dont put /end if its not present in the original'

    response = textgeneration(prompt)
    print(response)

def resumeGenerator(resume_location, website_url = "https://www.karkidi.com/job-details/43057-co-op-software-engineer-job"):
    jobposting = scrape_text_jobposting(website_url)
    jp = extract_jobdescription(jobposting)
    extracted_resume= extract_resume(resume_location)
    resume = pre_process()
    print("Generating Text")
    resume_ = generate_resume(resume,jp,extracted_resume)
    (conver_to_latex(resume_))