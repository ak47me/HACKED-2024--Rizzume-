from flask import Flask, request, render_template, send_file
from openai import OpenAI
from pathlib import Path
from bs4 import BeautifulSoup
import requests

# import my stt.py and tts.py files
from stt import speech_to_text as stt
# from generate import generate

app = Flask(__name__)

def scrapeJobDescription():
    url = "https://www.karkidi.com/job-details/43057-co-op-software-engineer-job?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    jobDescription = soup.get_text()
    client = OpenAI(api_key="your api key")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": "You are a smart job description finder bot. You are given a long text and you need to find the text in the entire webpage that is the job description, job responsibilities, job requirements, or any synonyms that might be there alluring to these things. Basically we want to know what the job expects from the applicant. Return the result as a string."
            },
            {
                "role": "user",
                "content": jobDescription
            }

        ]
    )
    replyContent = response.choices[0].message.content
    return replyContent

jobDescription = scrapeJobDescription()
print(jobDescription)
messageHistory = []
messageHistory.append({"role": "system", "content": f"You are interviewing a candidate for a position at a job. The job description is this: {jobDescription}. I want you to act as an interviewer. I want you to only reply as the interviewer. Ask the candidate the questions and wait for their answers. After asking 5 questions, give feedback on the quality of the answers. Then say “Thank you for meeting with me to chat about this opportunity. I will be in touch with you soon.”"})

@app.route('/')
def index():
    return render_template('interview.html')

@app.route('/save', methods=['POST'])
def save():
    file = request.files['file']
    file.save('recorded_audio.mp3')

    userSpeech = stt("recorded_audio.mp3")
    print(userSpeech)    
    client = OpenAI(api_key="your api key")
    messageHistory.append({"role": "user", "content": userSpeech})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messageHistory,
        )
    replyContent = response.choices[0].message.content
    messageHistory.append({"role": "assistant", "content": replyContent})
    
    speech_file_path = Path(__file__).parent / "gptreply.mp3"
    audioResponse = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input= replyContent,
    )
    audioResponse.stream_to_file(speech_file_path)

    return send_file(speech_file_path, mimetype="audio/mp3")


if __name__ == "__main__":
    app.run(debug=True)
    
