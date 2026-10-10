from requests import get
import os
from dotenv import load_dotenv

load_dotenv()

try:
    domain_url = os.environ["domain_url"]
except KeyError:
    print("Error: 'domain_url' not found in environment variables.")
    domain_url = ""

def get_request(url: str) -> tuple[int, str, type]:
    response = get(url)
    return response.status_code, response.text, type(response)

try:
    response_code, response_text, response_type = get_request(domain_url)   
    print(f"Response Code: {response_code}")
    print(f"Response Text: {response_text}")
    print(f"Response Type: {response_type}")      
except Exception as e:
    print(f"An error occurred: {e}")