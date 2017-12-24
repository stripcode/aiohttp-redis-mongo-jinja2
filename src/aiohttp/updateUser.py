from requests import put

user = {
  "id": 1,
  "name": "Bob",
  "age": 21
}

r = put("http://localhost:8000/user/1", json = user)
print(r.status_code)
print(r.text)