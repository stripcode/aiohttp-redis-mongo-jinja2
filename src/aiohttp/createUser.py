from requests import post

user = {
  "id": 1,
  "name": "Bob",
  "age": 19
}

r = post("http://localhost:8000/user/", json = user)
print(r.status_code)
print(r.text)