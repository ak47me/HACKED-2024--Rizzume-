from flask import Flask, request, jsonify, send_file, render_template
import os
from openai import OpenAI
from pathlib import Path
from bs4 import BeautifulSoup
import requests

from stt import speech_to_text as stt
from resumeParser import resumeGenerator, coverLetter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ''

def scrapeJobDescription():
    url = "https://www.karkidi.com/job-details/43057-co-op-software-engineer-job?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    jobDescription = soup.get_text()
    client = OpenAI(api_key="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")
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

@app.route('/resume', methods=['POST'])
def process_data():
    file = request.files['file']
    text1 = request.form.get('text1')
    text2 = request.form['text2']
    if (file):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename) 
        if text2 == "Submit resume":
            coverLetter(file)
        if text2 == "Submit Resume":
            resumeGenerator(filename)
        return "Successfully Uploaded"
    return "Error"

@app.route('/resumeFile', methods=['GET'])
def resume_file():
    return send_file('test.pdf', mimetype='application/pdf')

@app.route('/save', methods=['POST'])
def save():
    file = request.files['file']
    print(file)
    file.save('recorded_audio.mp3')
    audioGenerate()
    return "Generated Successfully"

def audioGenerate():
    userSpeech = stt("recorded_audio.mp3")
    client = OpenAI(api_key="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")
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
    return 

@app.route('/audioFile', methods=['GET'])
def getAudio():
    file_path = "gptreply.mp3"
    print("file_path")
    return send_file(file_path, mimetype="audio/mp3")

if __name__ == '__main__':
    app.run(debug=True)
