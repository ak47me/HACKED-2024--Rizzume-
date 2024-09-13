
# Rizzume

**Instantly Tailor Resumes and Cover Letters for Job Applications**

## Inspiration

One of our team members had a master resume and faced the repetitive task of manually tailoring resumes for each job application. This inspired us to create an automated solution that would save time and effort.

## What It Does

This Chrome extension offers three key features:

- **Resume Tailoring:** Instantly tailors your resume based on the job description you provide.
- **Cover Letter Customization:** Generates personalized cover letters matching the job requirements.
- **Job Interviewer:** A built-in interviewer that conducts mock interviews based on the job description, helping you prepare for your actual interview.

## How We Built It

We divided the project into three main tasks:

- **Client Side:** Developed using Flask.
- **Server Side:** Built as a Google Chrome extension.
- **Interaction:** Managed using JavaScript to connect Flask with the extension.

## Challenges We Ran Into

- Integrating Flask with the Chrome extension presented technical challenges.
- Handling the interaction between the client and server required careful planning and testing.

## Accomplishments

- Successfully hosted the extension on the Chrome Web Store.
- Established a functional connection between Flask and the Chrome extension.

## What We Learned

- Persistence is key; there were moments when we almost gave up on the project, but our determination saw us through.
- The importance of teamwork and dividing tasks effectively.

## Built With

- **Chrome** for the extension environment
- **CSS** for styling
- **Flask** for the client-side application
- **HTML** for structure
- **JavaScript** for interaction and functionality
- **OpenAI API** for resume, cover letter customization, and interview generation
- **Python** for backend scripting

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ak47me/rizzume.git
   ```

2. Navigate to the project directory:

   ```bash
   cd rizzume
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Load the extension into Chrome:
   - Go to `chrome://extensions/`.
   - Enable "Developer mode" on the top right.
   - Click "Load unpacked" and select the extension folder.

## Usage

- **Tailor Resumes:** Upload your resume and job description, and the extension will automatically adjust your resume.
- **Generate Cover Letters:** Provide a job description, and the extension will create a personalized cover letter for you.
- **Mock Interview:** Use the interviewer feature to simulate an interview based on the job description.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.


Let me know if you'd like any adjustments or additional information!
