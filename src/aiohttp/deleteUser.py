from requests import delete

r = delete("http://localhost:8000/user/1")
print(r.status_code)
print(r.text)