import requests
from bs4 import BeautifulSoup

def scrape_text(url):
    try:
        # Send an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text content
            text_content = soup.get_text()

            return text_content
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Replace 'your_website_url' with the actual URL of the webpage
website_url = 'https://jobs.netflix.com/jobs/307811529'
extracted_text = scrape_text(website_url)

if extracted_text:
    print(extracted_text)

with open("gettext.txt", 'w', encoding='utf-8') as file:
    file.write(extracted_text)