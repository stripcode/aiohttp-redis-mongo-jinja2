from requests import get

r = get("http://localhost:8000/user/1")
print(r.status_code)
print(r.text)