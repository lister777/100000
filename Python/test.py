class sampleclass: 
    count = 0     # class attribute 
        
    def __init__(self): 
        self.name = 'xyz'
        self.salary = 4000
  
    def show(self): 
        print self.name 
        print self.salary 
        
    def increase(self): 
        sampleclass.count += 1
        
s = sampleclass()
print(dir(s))
print(dir(s.__class__))