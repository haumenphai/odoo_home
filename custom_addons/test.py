import requests
from bs4 import BeautifulSoup



class Dog():
    def hello(self):
        print('dog hello ')

class Cat(Dog):
    def hello(self):
        super(Cat, self).hello()
        print('cat hello')

cat = Cat()
cat.hello()