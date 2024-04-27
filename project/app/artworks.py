import requests
import random
def artwork():
    li = [34,37,38,39,40,41,
     42,
     43,
     44,
     45,
     46,
     47,
     50,
     51,
     52,
     53,
     56,
     57,
     62,

     63,
     64,
     65,
     68,
     69,
     70,
     71,
     74,
     75,
     78,
     79,
     80,
     81,
     86,
     87,
     88,
     89,
     90,
     91,
     92,
     93,
     94,
     95]
    i = random.choice(li)
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}"
    response = requests.get(url)
    return response.json()
    