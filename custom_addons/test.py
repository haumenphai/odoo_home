import requests
from bs4 import BeautifulSoup
"""
ip = request.httprequest.environ.get('HTTP_X_REAL_IP', request.httprequest.remote_addr)
print('IP', ip)
# ip = '14.241.100.103'
ip = '72.229.28.185'
data = requests.get(f'https://geolocation-db.com/json/{ip}').json()
country_code = data['country_code']
print('country_code', country_code)
"""



class Dog():
    def hello(self):
        print('dog hello ')

class Cat(Dog):
    def hello(self):
        super(Cat, self).hello()
        print('cat hello')

cat = Cat()
cat.hello()