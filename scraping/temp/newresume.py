import openai
API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY


with open("jobpostingdownload.txt", 'r') as file:
    jobposting = file.read()

with open("resume-extracted.txt",'r') as file:
    resume = file.read()

with open("latexformat.txt",'r') as file:
    latexformat = file.read()


prompt = f"Generate a customized subset of my master resume {resume} that closely matches the requirements of the following job posting:{jobposting} Please focus on highlighting relevant skills, experiences, and qualifications from my master resume that align with the key responsibilities and qualifications mentioned in the job posting."
response = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}]
)

print(response)

