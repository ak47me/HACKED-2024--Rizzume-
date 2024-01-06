import openai
import re
API_KEY = open("API_KEY", "r").read()

openai.api_key = API_KEY
with open("gettext.txt",'r', encoding='utf-8') as file:
    textscrap = file.read()

prompt = f'You are given this job description {textscrap}, give me a json file with the following parameters only: requirements, skills, job description, responsibilities, programming languages .'

response = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}]
)
content = response["choices"][0]["message"]["content"]


pattern = r'```(.*?)```'
matches = re.findall(pattern, content, re.DOTALL)

with open("jobpostingdownload.txt",'w') as file:
    file.write(str(content))
