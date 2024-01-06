# name, contact info, skills, experience, work experience, hyperlinks, awards and honors, volunteering
import re
from pdfminer.high_level import extract_text
import openai


API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY


text = extract_text("scraping/Resume.pdf")

prompt = f"Here is a resume: {text}, give me a python dictionary which has fields: name, contact information, skills, work experience, awards and honors, links, volunteering and if nothing is provided as a field set it to null"

response = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}]
)

content = response["choices"][0]["message"]["content"]
print(content)

pattern = r'{(.*?)}'
matches = re.findall(pattern, content, re.DOTALL)
print(matches)

with open("resume-extracted.txt",'w') as file:
    file.write(str(matches))


