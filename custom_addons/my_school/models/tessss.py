'''
Created on Apr 3, 2021

@author: do
'''
class Dog:
    def __init__(self):
        # self.name= name
        # self.age = age
        print('init dog')

    def hello(self):
        print('hello dog')
        
    a = 10



class DogV2():
    def hello(self):
        print('hello dogv2')
        
        
        
        
class Cat( DogV2, Dog):
    def __init__(self):
        print('init cat')
    
    
    def hello(self):
        # Dog.hello(self)
        super().hello()
        Dog.hello(self)
        print('hello cat')
        
Cat().hello()








