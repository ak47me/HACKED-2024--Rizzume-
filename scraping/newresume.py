import openai
import requests
from bs4 import BeautifulSoup
import re
from pdfminer.high_level import extract_text

resume_location = "scraping/Resume.pdf"


API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY

website_url = 'https://jobs.netflix.com/jobs/307811529' #job posting


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



            prompt = f'You are given this job description {text_content}, give me a json file with the following parameters only: requirements, skills, job description, responsibilities, programming languages .'

            content = textgeneration(prompt)

            with open("jobposting.txt", 'w', encoding='utf-8') as file:
                file.write(content)

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
    with open("temp/resume-extracted.txt", 'w') as file:
        file.write(content)


# reading all files
def generate_resume():
    with open("jobposting.txt", 'r') as file:
        jobposting = file.read()

    with open("temp/resume-extracted.txt", 'r') as file:
        resume = file.read()

    with open("resumeformat.txt", 'r') as file:
        resumeformat = file.read()


    prompt = f"Generate a customized subset of my master resume {resume} that closely matches the requirements of the following job posting:{jobposting} Please focus on highlighting relevant skills, experiences, and qualifications from my master resume that align with the key responsibilities and qualifications mentioned in the job posting and use the format given in {resumeformat}"
    response = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}]
    )

    print(response)


scrape_text_jobposting(website_url)
extract_resume(resume_location)
generate_resume()
