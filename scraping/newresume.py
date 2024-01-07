import openai
import requests
from bs4 import BeautifulSoup
import re
from pdfminer.high_level import extract_text
import json

resume_location = "scraping/Resume.pdf"


API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY

website_url = 'https://www.livehire.com/careers/enbridge/job/FNDPA/B1XJTNONV/ot-software-systems-analyst-co-op-student' #job posting


def textgeneration(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}])

    return response["choices"][0]["message"]["content"]

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
            print("Text from soup: ",text_content)

            prompt = f'You are given this job description {text_content}, give me a json file with the following parameters only: requirements, skills, job description, responsibilities, programming languages .'

            content = textgeneration(prompt)
            print("GPT simplified: ",content)
            print(type(content))
            #print(content)
            return content

        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



# pattern = r'```(.*?)```'
# matches = re.findall(pattern, content, re.DOTALL)

# with open("jobpostingdownload.txt",'w') as file:
#     file.write(str(content))

# extracting resume and using GPT to refine
def extract_resume(resume_location):
    text = extract_text(resume_location)
    prompt = f"Here is a resume: {text}, give me a python dictionary which has fields: name, contact information, skills, work experience, awards and honors, links, volunteering and if nothing is provided as a field set it to null"
    content = textgeneration(prompt)
    print("Extracted resume: ", content)
    return content


# reading all files
def generate_resume(jobposting,extracted_resume):



    prompt = f"Generate a customized subset of my master resume {extracted_resume} that closely matches the requirements of the following job posting:{jobposting} Please focus on highlighting relevant skills, experiences, and qualifications from my master resume that align with the key responsibilities and qualifications mentioned in the job posting."

    response = textgeneration(prompt)
    print(response)
    return response

def conver_to_latex(resume):
    with open("resumeformat.txt", 'r') as file:
        resumeformat = file.read()
    prompt = f'Convert this resume {resume} into latex using the following template {resumeformat} make sure to put everything from the resume I provided.'

    response = textgeneration(prompt)
    print(response)

def create_cover_letter(jobposting,extracted_resume):
    prompt = f'Based on this job posting: {jobposting} and my resume: {extracted_resume} make me a cover letter for this job'
    content = textgeneration(prompt)
    print("Cover Letter: ")
    return content

def extract_jobdescription(jobposting):
    extrated_posting = {"requirements":[], "skills":[], "job description":[],"responsibilities":[],"programming languages":[]}
    extrated_posting["requirements"] = textgeneration(f'Give me only the requirements of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the requirements')
    extrated_posting["skills"] = textgeneration(f'Give me only the skills of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the skills')
    extrated_posting["job description"] = textgeneration(f'Give me only the job description of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the job description')
    extrated_posting["responsibilities"] = textgeneration(f'Give me only the responsibilities of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the job description')
    extrated_posting["programming languages"] = textgeneration(f'Give me only the programming languages of this job posting: {jobposting} from this json file and no extra preecding or trailing words other than the programming languages')
    print(extrated_posting)
    return extrated_posting





jobposting = scrape_text_jobposting(website_url)
extract_jobdescription(jobposting)
extracted_resume= extract_resume(resume_location)
resume = generate_resume(jobposting,extracted_resume)

#conver_to_latex(resume)
#extract_json_file(jobposting)


