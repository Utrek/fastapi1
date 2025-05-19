import requests


data = requests.post("http://127.0.0.1:8000/api/v1/advert", json={
    "title": "Red_horse",
    "price": 1.66,
    "description": "carrion",
    "author": "not_man"})

data = requests.get("http://127.0.0.1:8000/api/v1/advert/3")

data = requests.patch("http://127.0.0.1:8000/api/v1/advert/1", json={
    "title": "Gray_horse",
    "price": 1999.99,
    "description": "A strong old wise horse, suitable for plough work",
    "author": "Dad_man"})

data = requests.get("http://127.0.0.1:8000/api/v1/advert/", params={"title": "Gray_horse"})

data = requests.delete("http://127.0.0.1:8000/api/v1/advert/3")
print(data.status_code)
print(data.json())
