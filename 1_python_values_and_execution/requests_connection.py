from requests import get

def get_request(url):
    response = get(url)
    return response.status_code, response.text, type(response)

response_code, response_text, response_type = get_request("https://api.github.com/users/hadley/orgs")   

print(f"Response Code: {response_code}")
print(f"Response Text: {response_text}")
print(f"Response Type: {response_type}")      
