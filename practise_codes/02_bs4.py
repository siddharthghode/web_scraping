import requests
from bs4 import BeautifulSoup


url = "https://www.freepsychotherapybooks.org/?gad_source=1&gad_campaignid=345902298&gbraid=0AAAAADwA1k79tGEAnV_wIOk7tOQQSGFqE&gclid=CjwKCAjwgO7RBhBKEiwAZNP85sbYvVWeMjs3-fwQ5zNV7xBf-CLnEKnbObYtN2yKukMqf8jSHvs_ExoCLIgQAvD_BwE"

response = requests.get(url)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

script = soup.find(id="signupScript")

print(script)