import requests
import random
from requests.auth import HTTPBasicAuth
from auth import img_client_id, img_client_secret

dog = ('dogs',
       'corgi',
       'wigglebutts',
       'dogswithjobs',
       'blop',
       'whatswrongwithyourdog',
       'puppysmiles',
       'dogshowerthoughts')

cat = ('blep',
       'CatsStandingUp',
       'JellyBeanToes',
       'kittens',
       'CatsInBusinessAttire',
       'CatsonGlass',
       'CatsInSinks',
       'CatLoaf',
       'Cats')

def get_imglink(subject):
    sort = 'time'
    window = 'day'
    page = 0
    headers = {'Authorization' : f'Client-ID {img_client_id}'}

    rand_sub = random.randrange(0, 8)
    r = requests.get(f"https://api.imgur.com/3/gallery/r/{subject[rand_sub]}/{sort}/{window}/{page}", headers=headers)
    data = r.json()

    rand_link = random.randrange(1, 101)
    img_link = data['data'][rand_link]['link']

    return img_link

#def main():

#    with open('cats.txt', 'w') as f:
#
#        for x in range(10):
#            img_link = get_imglink(cat)
#            f.write(f'{img_link}\n')

if(__name__ == "__main__"):
    main()