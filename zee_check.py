import requests

url = "https://zeenews.india.com/hindi"
response = requests.get(url)

print(f"Status Code: {response.status_code}")
print("Response Content (first 500 chars):\n", response.text[:500])
